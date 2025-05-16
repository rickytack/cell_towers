#include <vector>
#include <memory>
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Delaunay_triangulation_2.h>
#include <CGAL/Triangulation_vertex_base_with_info_2.h>

#include "task_worker_service.h"

// CGAL typedefs
using K = CGAL::Exact_predicates_inexact_constructions_kernel;
using Vb = CGAL::Triangulation_vertex_base_with_info_2<uint32_t, K>;
using Tds = CGAL::Triangulation_data_structure_2<Vb>;
using Delaunay = CGAL::Delaunay_triangulation_2<K, Tds>;
using Point = K::Point_2;


namespace task_worker
{
Status TaskWorkerService::Process(ServerContext* context, const TaskRequest* request, TaskResponse* response)
{

    // 1. Log incoming request
    std::cout << "Received task type: " << TaskType_Name(request->task_type()) << std::endl;
    std::cout << "Processing " << request->points_size() << " points" << std::endl;

    // 2. Process based on task type
    switch (request->task_type())
    {
    case TaskType::TRIANGULATION:
        handleTriangulation(request, response);
        break;

    default:
        return Status(grpc::StatusCode::INVALID_ARGUMENT, "Unknown task type");
    }

    return Status::OK;
}

void TaskWorkerService::handleTriangulation(const TaskRequest* request, TaskResponse* response)
{
    std::cout << request->points_size() << "!!! request->points_size()" << std::endl;

    // Extract points from the request
    const auto& points = request->points();

    // We need at least 3 points for triangulation
    if (points.size() < 3) {
        // Not enough points - return empty response
        return;
    }

    // Prepare input for CGAL triangulation
    std::vector<std::pair<Point, uint32_t>> cgal_points;
    cgal_points.reserve(points.size());

    for (uint32_t i = 0; i < points.size(); ++i) {
        const auto& point = points[i];
        cgal_points.emplace_back(Point(point.lng(), point.lat()), i);
    }

    // Perform Delaunay triangulation
    Delaunay dt;
    dt.insert(cgal_points.begin(), cgal_points.end());

    // Prepare the response
    PolygonResult* polygon_result = response->mutable_polygons();

    // Iterate through all finite faces (triangles) in the triangulation
    for (auto face = dt.finite_faces_begin(); face != dt.finite_faces_end(); ++face) {
        Polygon* polygon = polygon_result->add_polygons();

        // Add all three vertices of the triangle
        for (int i = 0; i < 3; ++i) {
            auto vertex = face->vertex(i);
            GeoPoint* gp = polygon->add_vertices();
            gp->set_lat(vertex->point().y());
            gp->set_lng(vertex->point().x());

//            // Copy the original value if it exists
//            uint32_t idx = vertex->info();
//            if (idx < points.size()) {
//                gp->set_value(points[idx].value());
//            }
        }

        // Calculate and set the area of the triangle
        auto& a = face->vertex(0)->point();
        auto& b = face->vertex(1)->point();
        auto& c = face->vertex(2)->point();
        double area = CGAL::abs(CGAL::area(a, b, c));
        polygon->set_area(static_cast<float>(area));
    }
}
} // namespace task_worker
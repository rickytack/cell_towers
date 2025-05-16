//
// Created by solomin on 11.05.25.
//

#ifndef TASK_WORKER_TASK_WORKER_SERVICE_H
#define TASK_WORKER_TASK_WORKER_SERVICE_H

#include <grpcpp/grpcpp.h>

#include "../generated/task_worker.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
namespace task_worker {

class TaskWorkerService final : public TaskWorker::Service {
public:
  Status Process(ServerContext *context, const TaskRequest *request,
                 TaskResponse *response) override;

private:
  static void handleTriangulation(const TaskRequest *request,
                                  TaskResponse *response);
};
} // namespace task_worker

#endif // TASK_WORKER_TASK_WORKER_SERVICE_H

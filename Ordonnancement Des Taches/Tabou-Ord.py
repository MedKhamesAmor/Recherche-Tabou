import random


class JobShopSchedulingTabou:
    def __init__(self, jobs):
        self.jobs = jobs
        self.num_machines = max(machine for job in jobs.values() for machine, _ in job) + 1
        self.num_jobs = len(jobs)

    def decode_schedule(self, operation_sequence):
        machine_times = [0] * self.num_machines
        job_times = [0] * (self.num_jobs + 1)
        schedule = []
        makespan = 0

        for job_id, op_num in operation_sequence:
            machine, duration = self.jobs[job_id][op_num]
            start_time = max(machine_times[machine], job_times[job_id])
            end_time = start_time + duration
            machine_times[machine] = end_time
            job_times[job_id] = end_time

            schedule.append({
                'job': job_id, 'operation': op_num, 'machine': machine,
                'start': start_time, 'end': end_time, 'duration': duration
            })
            makespan = max(makespan, end_time)

        return schedule, makespan

    def generate_initial_solution(self):
        operations = []
        for job_id in self.jobs:
            for op_num in range(len(self.jobs[job_id])):
                operations.append((job_id, op_num))
        random.shuffle(operations)
        return operations

    def get_all_neighbors(self, current_sequence):
        neighbors = []
        machine_ops = {}

        for i, (job_id, op_num) in enumerate(current_sequence):
            machine = self.jobs[job_id][op_num][0]
            if machine not in machine_ops:
                machine_ops[machine] = []
            machine_ops[machine].append(i)

        for machine in machine_ops:
            if len(machine_ops[machine]) >= 2:
                indices = machine_ops[machine]
                for i in range(len(indices)):
                    for j in range(i + 1, len(indices)):
                        neighbor = current_sequence.copy()
                        idx1, idx2 = indices[i], indices[j]
                        neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
                        neighbors.append(neighbor)

        return neighbors

    def recherche_tabou(self, tabu_size=10, max_iterations=100):
        current_solution = self.generate_initial_solution()
        current_schedule, current_makespan = self.decode_schedule(current_solution)
        best_solution = current_solution.copy()
        best_schedule = current_schedule
        best_makespan = current_makespan

        tabu_list = []

        print(f"Starting Tabou Search with makespan: {current_makespan}")

        for iteration in range(max_iterations):
            neighbors = self.get_all_neighbors(current_solution)
            best_neighbor = None
            best_neighbor_makespan = float('inf')

            for neighbor in neighbors:
                neighbor_schedule, neighbor_makespan = self.decode_schedule(neighbor)

                if neighbor_makespan < best_neighbor_makespan:
                    if neighbor not in tabu_list:
                        best_neighbor = neighbor
                        best_neighbor_makespan = neighbor_makespan
                    elif neighbor_makespan < best_makespan:
                        best_neighbor = neighbor
                        best_neighbor_makespan = neighbor_makespan

            if best_neighbor is None:
                break

            current_solution = best_neighbor
            current_schedule, current_makespan = self.decode_schedule(current_solution)

            tabu_list.append(best_neighbor)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            if current_makespan < best_makespan:
                best_solution = current_solution.copy()
                best_schedule = current_schedule
                best_makespan = current_makespan

            if iteration % 20 == 0:
                print(f"Iteration {iteration}: Best makespan={best_makespan}, Tabu list size={len(tabu_list)}")

        print(f"Finished with best makespan: {best_makespan}")
        return best_solution, best_schedule, best_makespan


# Example usage with the same problem
if __name__ == "__main__":
    jobs = {
        1: [(0, 3), (1, 2), (2, 2)],
        2: [(0, 2), (2, 1), (1, 4)],
        3: [(1, 4), (0, 3), (2, 1)],
    }

    job_shop_tabou = JobShopSchedulingTabou(jobs)
    best_solution, best_schedule, best_makespan = job_shop_tabou.recherche_tabou()

    print("\nBest schedule:")
    for op in best_schedule:
        print(
            f"Job {op['job']}, Operation {op['operation']}: Machine {op['machine']} from {op['start']} to {op['end']}")
from typing import Counter
from Table import Table
from time import time

class Particle:
    def __init__(self, id: int, pos: list, vel: list, acc: tuple):
        self.id = id
        self.position = pos
        self.velocity = vel
        self.acceleration = acc

    def update(self):
        self.velocity[0] = self.velocity[0] + self.acceleration[0]
        self.velocity[1] = self.velocity[1] + self.acceleration[1]
        self.velocity[2] = self.velocity[2] + self.acceleration[2]

        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]
        self.position[2] = self.position[2] + self.velocity[2]

    def distance(self):
        return sum([abs(val) for val in self.position])

    def comb_acc(self):
        return sum([dim**2 for dim in self.acceleration])

class Day20(Table):

    def __init__(self):
        self.day = 20
        self.title = "Particle Swarm"
        self.input = self.getInput(self.day)

    def get_particles(self):
        particles = []
        for id, line in enumerate(self.input.splitlines()):
            pos, vel, acc = line.split(', ')

            pos = [int(val) for val in pos[3:-1].split(',')]
            vel = [int(val) for val in vel[3:-1].split(',')]
            acc = [int(val) for val in acc[3:-1].split(',')]

            particles.append(Particle(id, pos, vel, tuple(acc)))

        return particles

    def solve(self):
        start_time = time()

        particles = self.get_particles()

        # the particle that stays closest to 0,0,0 in the long term is the particle with the lowest combined acceleration
        min_acc = min([particle.comb_acc() for particle in particles])
        slowest_particles = [particle.id for particle in particles if particle.comb_acc() == min_acc]

        part1 = slowest_particles[0]

        for _ in range(50):
            for particle in particles:
                particle.update()

            common_positions = Counter([tuple(particle.position) for particle in particles]).most_common()
            i = 0
            while True:
                position, count = common_positions[i]
                if count == 1:
                    break

                particles_to_remove = [particle for particle in particles if tuple(particle.position) == position]
                for particle_to_remove in particles_to_remove:
                    particles.remove(particle_to_remove)

                i += 1

        part2 = len(particles)

        end_time = time()
        seconds_elapsed = end_time - start_time

        return (self.day, self.title, part1, part2, seconds_elapsed)


if __name__ == "__main__":
    day = Day20()
    day.printRow(day.headers())
    day.printRow(day.solve())
    print("")

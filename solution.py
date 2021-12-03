from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        n = self.read_input()
        step = n / len(self.workers)
        mapped = []
        odd = len(self.workers) - 1

        for i in xrange(0, len(self.workers)-1):
            mapped.append(self.workers[i].mymap(i * step, i * step + step, len(self.workers)))


        mapped.append(self.workers[odd].mymap(odd * step, n, len(self.workers)))

        print('Map finished: ', mapped)

        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        self.write_output(reduced)
        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b, N):
        print (a, b)
        eps = 10**(-4)/N
        dx = 0.05
        prev_res = eps + 1.0
        res = Solver.integral(a, b, dx)
        while abs(res - prev_res) > eps:
            prev_res = res
            dx = dx/2
            n = int((b - a) / dx)
            res = Solver.integral(a, b, dx)
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = 0.0
        for x in mapped:
            output += float(x.value)
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()

    @staticmethod
    @expose
    def integral(a, b, dx):
        if a > b:
            a, b = b, a
        n = int((b - a) / dx)
        s = 0.0
        x = a
        for i in xrange(n):
            f_i = x**(0.5) + 1
            s += f_i
            x += dx
        return s * dx

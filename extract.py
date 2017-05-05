
class Ensemble(object):
    def __init__(self, name, tau_rc, tau_ref, n_neurons, dims):
        self.name = name
        self.tau_rc = tau_rc
        self.tau_ref = tau_ref
        self.n_neurons = n_neurons
        self.dims = dims
        self.connections = {}
    def add(self, decoder, target_name, transform, synapse):
        if synapse not in self.connections:
            self.connections[synapse] = set()
        self.connections[synapse].add(target_name)


class Reader(object):
    def __init__(self, filename):
        self.ensembles = {}
        self.read(open(filename))

    def total_neurons(self):
        return sum(ens.n_neurons for ens in self.ensembles.values())

    def read(self, f):
        ens = None
        for line in f.readlines():
            if line.startswith(' '):
                line = line.strip()
                decoder, target = line.split(', ', 1)
                assert target[0] == '['
                assert target[-1] == ']'
                target = target[1:-2]
                if len(target) > 0:
                    targets = target.split('),')
                    for t in targets:
                        t = t[1:]
                        name, t = t.split(', ', 1)
                        transform, synapse = t.rsplit(', ', 1)
                        ens.add(decoder, name, transform, synapse)
            else:
                data = line.strip().split(', ')
                name, tau_rc, tau_ref, n_neurons, dims = data
                print name
                ens = Ensemble(name=name,
                               tau_rc=float(tau_rc),
                               tau_ref=float(tau_ref),
                               n_neurons=int(n_neurons),
                               dims=int(dims))
                assert name not in self.groups
                self.ensembles[name] = ens


r = Reader('spaun-v5.txt')
print r.total_neurons()


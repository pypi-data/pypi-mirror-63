import os
import typing

import requests
import numpy as np

from feyn import Graph, QGraph


class Register:
    """
    Registers are the main interaction point with the QLattice, IO interfaces.
    Users connect registers with their data concepts, columns in their dataset or stores.
    """
    def __init__(self, celltype, label, location) -> None:
        """Construct a new 'Register' object.

        Arguments:
            celltype {str} -- Either "cont" or "cat" (continous or categorical).
            label {str} -- Name of the register, so that you can find it again later.
                           Usually the column name in your dataset, or the name of the concept this register represents.
            location {tuple(int, int, int)} -- Location in the QLattice.
        """
        self.celltype = celltype
        self.label = label
        self.location = location

    def to_dict(self):
        return {
            'celltype': self.celltype,
            'label': self.label
        }


class QLattice:
    """
    The QLattice is a potentially very large lattice that links registers to
    each other through a set of interaction cells.

    QLattice incorporates all the knowledge learned about the probabilities of
    relations between registers and interaction cells.

    Through abzu algorithm we can extract QGraphs from the QLattice.
    """
    QLATTICE_BASE_URI = os.environ.get('QLATTICE_BASE_URI') or 'http://localhost:5000'

    def __init__(self, url=None, reset=False) -> None:
        """Construct a new 'QLattice' object.

        Keyword Arguments:
            url {str} -- URL of where your QLattice is running.
            reset {bool} -- Clears all learnings in the QLattice. Potentially very dangerous. Think twice before setting this to True! (default: {False})
        """
        if url is None:
            url = f"{self.QLATTICE_BASE_URI}/api/v1/qlattice"
        elif '/api/v1/qlattice' not in url:
            url = f"{url}/api/v1/qlattice"

        self.url = url

        self._load_qlattice(reset)
    
    def _add_register(self, label: str, register_type: str = "cont") -> Register:
        req = requests.put("%s/register" % self.url, json={
            'celltype': register_type,
            'label': label
        })
        req.raise_for_status()

        if req.status_code == 200:
            self._load_qlattice()

        reg = req.json()

        return Register(reg['celltype'], reg['label'], reg['location'])

    def fit(self, inputs, output, data, batches=10, epochs=10, steps=3):
        if not isinstance(data, tuple):
            raise ValueError("Data must be a tuple (X, y)")
        
        X = data[0]
        y = data[1]

        if batches <= 0:
            raise ValueError("Batch size must be at least 1")
        
        for b in range(batches+1):
            qgraph = self.get_qgraph(inputs, output, steps=steps)
            qgraph.tune(X, y, epochs=epochs, extra_info=f"Batch: {b}")
            best = qgraph.graphs[0]
            self.update(best)

            if b >= batches:
                return qgraph

    def add_register(self, label: typing.Union[str, typing.List[str]], register_type: str = "cont") -> typing.Union[Register, typing.List[Register]]:
        """Add a new register to QLattice, if the register already exists returns same
        instance.

        Arguments:
            label {typing.Union[str, typing.List]} -- Name/s for registers.
            register_type {str} -- Register type, either "cont" or "cat". (continous or categorical)

        Returns:
            Register -- The register instance.
        """

        if isinstance(label, (list, np.ndarray)):
            return [self._add_register(l, register_type) for l in label]  
        else:
            return self._add_register(label, register_type)

    def get_qgraph(self, inputs: typing.List[Register], output: Register, steps: int = 3) -> QGraph:
        """Extract QGraph from inputs registers to output register.

        Arguments:
            inputs {typing.List[Register]} -- Input registers.
            output {Register} -- Output register.

        Returns:
            QGraph -- The QGraph instance from the inputs to the output.
        """
        
        req = requests.post("%s/simulation" % self.url, json={
            'inputs': [reg.to_dict() for reg in inputs],
            'output': output.to_dict(),
            'steps': steps
        })

        req.raise_for_status()

        graph = req.json()

        qgraph = QGraph(graph)

        return qgraph

    def update(self, graph: Graph) -> None:
        """ Update QLattice with learnings from a graph.

        Arguments:
            graph {Graph} -- Graph with learnings worth storing.
        """
        req = requests.post("%s/update" % self.url,
                            json=graph._to_dict()
                            )

        req.raise_for_status()

    def _load_qlattice(self, reset=False):
        req = requests.get("%s" % self.url, params={'reset': reset})
        req.raise_for_status()
        qlattice = req.json()

        self.width = qlattice['width']
        self.height = qlattice['height']

        self.registers = [Register(reg['celltype'], reg['label'], reg['location']) for reg in qlattice['registers']]

    def __repr__(self):
        return "<Abzu QLattice[%i,%i] '%s'>" % (self.width, self.height, self.url)

from __future__ import absolute_import
import numpy
import forcebalance
import os, sys
import tarfile
import logging
import pytest
from .__init__ import ForceBalanceTestCase

logger = logging.getLogger("test")

class TestOptimizer(ForceBalanceTestCase):
    def setup_method(self, method):
        super().setup_method(method)
        self.cwd = os.path.dirname(os.path.realpath(__file__))
        os.chdir(os.path.join(self.cwd, '../../studies/001_water_tutorial'))
        self.input_file='very_simple.in'
        targets = tarfile.open('targets.tar.bz2','r')
        targets.extractall()
        targets.close()

        self.options, self.tgt_opts = forcebalance.parser.parse_inputs(self.input_file)

        self.options.update({'writechk':'checkfile.tmp'})

        self.forcefield  = forcebalance.forcefield.FF(self.options)
        self.objective   = forcebalance.objective.Objective(self.options, self.tgt_opts, self.forcefield)
        try: self.optimizer   = forcebalance.optimizer.Optimizer(self.options, self.objective, self.forcefield)
        except: pytest.fail("\nCouldn't create optimizer")

    def teardown_method(self):
        os.system('rm -rf result *.bak *.tmp')
        super().teardown_method()

    def test_optimizer(self):
        self.optimizer.writechk()
        assert os.path.isfile(self.options['writechk']), "Optimizer.writechk() didn't create expected file at %s " % self.options['writechk']
        read = self.optimizer.readchk()
        assert isinstance(read, dict)

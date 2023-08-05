"""CmdStan method sample tests"""

import os
import logging
import shutil
from multiprocessing import cpu_count
import unittest
from testfixtures import LogCapture
import pytest

from cmdstanpy.cmdstan_args import Method, SamplerArgs, CmdStanArgs
from cmdstanpy.utils import EXTENSION
from cmdstanpy.stanfit import RunSet, CmdStanMCMC
from cmdstanpy.model import CmdStanModel

HERE = os.path.dirname(os.path.abspath(__file__))
DATAFILES_PATH = os.path.join(HERE, 'data')
GOODFILES_PATH = os.path.join(DATAFILES_PATH, 'runset-good')
BADFILES_PATH = os.path.join(DATAFILES_PATH, 'runset-bad')


class SampleTest(unittest.TestCase):

    # pylint: disable=no-self-use
    @pytest.fixture(scope='class', autouse=True)
    def do_clean_up(self):
        for root, _, files in os.walk(DATAFILES_PATH):
            for filename in files:
                _, ext = os.path.splitext(filename)
                if ext.lower() in ('.o', '.hpp', '.exe', ''):
                    filepath = os.path.join(root, filename)
                    os.remove(filepath)

    def test_bernoulli_good(self, stanfile='bernoulli.stan'):
        stan = os.path.join(DATAFILES_PATH, stanfile)
        bern_model = CmdStanModel(stan_file=stan)

        jdata = os.path.join(DATAFILES_PATH, 'bernoulli.data.json')
        bern_fit = bern_model.sample(
            data=jdata, chains=4, cores=2, seed=12345, iter_sampling=100
        )
        self.assertIn('CmdStanMCMC: model=bernoulli', bern_fit.__repr__())
        self.assertIn('method=sample', bern_fit.__repr__())

        self.assertEqual(bern_fit.runset._args.method, Method.SAMPLE)

        for i in range(bern_fit.runset.chains):
            csv_file = bern_fit.runset.csv_files[i]
            stdout_file = bern_fit.runset.stdout_files[i]
            self.assertTrue(os.path.exists(csv_file))
            self.assertTrue(os.path.exists(stdout_file))

        self.assertEqual(bern_fit.runset.chains, 4)
        self.assertEqual(bern_fit.draws, 100)
        column_names = [
            'lp__',
            'accept_stat__',
            'stepsize__',
            'treedepth__',
            'n_leapfrog__',
            'divergent__',
            'energy__',
            'theta',
        ]
        self.assertEqual(bern_fit.column_names, tuple(column_names))

        bern_sample = bern_fit.sample
        self.assertEqual(bern_sample.shape, (100, 4, len(column_names)))
        self.assertEqual(bern_fit.metric_type, 'diag_e')
        self.assertEqual(bern_fit.stepsize.shape, (4,))
        self.assertEqual(bern_fit.metric.shape, (4, 1))

        bern_fit = bern_model.sample(
            data=jdata,
            chains=4,
            cores=2,
            seed=12345,
            iter_sampling=100,
            output_dir=DATAFILES_PATH,
        )
        for i in range(bern_fit.runset.chains):
            csv_file = bern_fit.runset.csv_files[i]
            stdout_file = bern_fit.runset.stdout_files[i]
            self.assertTrue(os.path.exists(csv_file))
            self.assertTrue(os.path.exists(stdout_file))
        bern_sample = bern_fit.sample
        self.assertEqual(bern_sample.shape, (100, 4, len(column_names)))
        for i in range(bern_fit.runset.chains):  # cleanup datafile_path dir
            os.remove(bern_fit.runset.csv_files[i])
            if os.path.exists(bern_fit.runset.stdout_files[i]):
                os.remove(bern_fit.runset.stdout_files[i])
            if os.path.exists(bern_fit.runset.stderr_files[i]):
                os.remove(bern_fit.runset.stderr_files[i])
        rdata = os.path.join(DATAFILES_PATH, 'bernoulli.data.R')
        bern_fit = bern_model.sample(
            data=rdata, chains=4, cores=2, seed=12345, iter_sampling=100
        )
        bern_sample = bern_fit.sample
        self.assertEqual(bern_sample.shape, (100, 4, len(column_names)))

        data_dict = {'N': 10, 'y': [0, 1, 0, 0, 0, 0, 0, 0, 0, 1]}
        bern_fit = bern_model.sample(
            data=data_dict, chains=4, cores=2, seed=12345, iter_sampling=100
        )
        bern_sample = bern_fit.sample
        self.assertEqual(bern_sample.shape, (100, 4, len(column_names)))

    def test_init_types(self):
        stan = os.path.join(DATAFILES_PATH, 'bernoulli.stan')
        bern_model = CmdStanModel(stan_file=stan)
        jdata = os.path.join(DATAFILES_PATH, 'bernoulli.data.json')

        bern_fit = bern_model.sample(
            data=jdata, chains=4, cores=2, seed=12345, iter_sampling=100,
            inits=1.1
        )
        self.assertIn('init=1.1', bern_fit.runset.__repr__())

        bern_fit = bern_model.sample(
            data=jdata, chains=4, cores=2, seed=12345, iter_sampling=100,
            inits=1
        )
        self.assertIn('init=1', bern_fit.runset.__repr__())

        with self.assertRaises(ValueError):
            bern_model.sample(
                data=jdata, chains=4, cores=2, seed=12345, iter_sampling=100,
                inits=(1, 2)
            )

        with self.assertRaises(ValueError):
            bern_model.sample(
                data=jdata, chains=4, cores=2, seed=12345, iter_sampling=100,
                inits=-1
            )

    def test_bernoulli_bad(self):
        stan = os.path.join(DATAFILES_PATH, 'bernoulli.stan')
        bern_model = CmdStanModel(stan_file=stan)

        with self.assertRaisesRegex(RuntimeError, 'variable does not exist'):
            bern_model.sample(
                chains=4, cores=2, seed=12345, iter_sampling=100
            )

        with self.assertRaisesRegex(RuntimeError, 'variable does not exist'):
            bern_model.sample(
                data={'foo': 1},
                chains=4, cores=2, seed=12345, iter_sampling=100
            )

    def test_multi_proc(self):
        logistic_stan = os.path.join(DATAFILES_PATH, 'logistic.stan')
        logistic_model = CmdStanModel(stan_file=logistic_stan)
        logistic_data = os.path.join(DATAFILES_PATH, 'logistic.data.R')

        with LogCapture() as log:
            logging.getLogger()
            logistic_model.sample(data=logistic_data, chains=4, cores=1)
        log.check_present(
            ('cmdstanpy', 'INFO', 'finish chain 1'),
            ('cmdstanpy', 'INFO', 'start chain 2'),
        )
        with LogCapture() as log:
            logging.getLogger()
            logistic_model.sample(data=logistic_data, chains=4, cores=2)
        if cpu_count() >= 4:
            # finish chains 1, 2 before starting chains 3, 4
            log.check_present(
                ('cmdstanpy', 'INFO', 'finish chain 1'),
                ('cmdstanpy', 'INFO', 'start chain 4'),
            )
        if cpu_count() >= 4:
            with LogCapture() as log:
                logging.getLogger()
                logistic_model.sample(data=logistic_data, chains=4, cores=4)
                log.check_present(
                    ('cmdstanpy', 'INFO', 'start chain 4'),
                    ('cmdstanpy', 'INFO', 'finish chain 1'),
                )

    def test_fixed_param_good(self):
        stan = os.path.join(DATAFILES_PATH, 'datagen_poisson_glm.stan')
        datagen_model = CmdStanModel(stan_file=stan)
        no_data = {}
        datagen_fit = datagen_model.sample(
            data=no_data, seed=12345, iter_sampling=100, fixed_param=True
        )
        self.assertEqual(datagen_fit.runset._args.method, Method.SAMPLE)

        for i in range(datagen_fit.runset.chains):
            csv_file = datagen_fit.runset.csv_files[i]
            stdout_file = datagen_fit.runset.stdout_files[i]
            self.assertTrue(os.path.exists(csv_file))
            self.assertTrue(os.path.exists(stdout_file))

        self.assertEqual(datagen_fit.runset.chains, 1)

        column_names = [
            'lp__',
            'accept_stat__',
            'N',
            'y_sim.1',
            'y_sim.2',
            'y_sim.3',
            'y_sim.4',
            'y_sim.5',
            'y_sim.6',
            'y_sim.7',
            'y_sim.8',
            'y_sim.9',
            'y_sim.10',
            'y_sim.11',
            'y_sim.12',
            'y_sim.13',
            'y_sim.14',
            'y_sim.15',
            'y_sim.16',
            'y_sim.17',
            'y_sim.18',
            'y_sim.19',
            'y_sim.20',
            'x_sim.1',
            'x_sim.2',
            'x_sim.3',
            'x_sim.4',
            'x_sim.5',
            'x_sim.6',
            'x_sim.7',
            'x_sim.8',
            'x_sim.9',
            'x_sim.10',
            'x_sim.11',
            'x_sim.12',
            'x_sim.13',
            'x_sim.14',
            'x_sim.15',
            'x_sim.16',
            'x_sim.17',
            'x_sim.18',
            'x_sim.19',
            'x_sim.20',
            'pop_sim.1',
            'pop_sim.2',
            'pop_sim.3',
            'pop_sim.4',
            'pop_sim.5',
            'pop_sim.6',
            'pop_sim.7',
            'pop_sim.8',
            'pop_sim.9',
            'pop_sim.10',
            'pop_sim.11',
            'pop_sim.12',
            'pop_sim.13',
            'pop_sim.14',
            'pop_sim.15',
            'pop_sim.16',
            'pop_sim.17',
            'pop_sim.18',
            'pop_sim.19',
            'pop_sim.20',
            'alpha_sim',
            'beta_sim',
            'eta.1',
            'eta.2',
            'eta.3',
            'eta.4',
            'eta.5',
            'eta.6',
            'eta.7',
            'eta.8',
            'eta.9',
            'eta.10',
            'eta.11',
            'eta.12',
            'eta.13',
            'eta.14',
            'eta.15',
            'eta.16',
            'eta.17',
            'eta.18',
            'eta.19',
            'eta.20'
        ]
        self.assertEqual(datagen_fit.column_names, tuple(column_names))
        self.assertEqual(datagen_fit.draws, 100)
        self.assertEqual(datagen_fit.sample.shape, (100, 1, len(column_names)))
        self.assertEqual(datagen_fit.metric, None)
        self.assertEqual(datagen_fit.metric_type, None)
        self.assertEqual(datagen_fit.stepsize, None)

    def test_bernoulli_file_with_space(self):
        self.test_bernoulli_good('bernoulli with space in name.stan')

    def test_bernoulli_path_with_space(self):
        self.test_bernoulli_good('path with space/'
                                 'bernoulli_path_with_space.stan')


class CmdStanMCMCTest(unittest.TestCase):
    def test_validate_good_run(self):
        # construct fit using existing sampler output
        exe = os.path.join(DATAFILES_PATH, 'bernoulli' + EXTENSION)
        jdata = os.path.join(DATAFILES_PATH, 'bernoulli.data.json')
        sampler_args = SamplerArgs(
            iter_sampling=100, max_treedepth=11, adapt_delta=0.95
        )
        cmdstan_args = CmdStanArgs(
            model_name='bernoulli',
            model_exe=exe,
            chain_ids=[1, 2, 3, 4],
            seed=12345,
            data=jdata,
            output_dir=DATAFILES_PATH,
            method_args=sampler_args,
        )
        runset = RunSet(args=cmdstan_args, chains=4)
        runset._csv_files = [
            os.path.join(DATAFILES_PATH, 'runset-good', 'bern-1.csv'),
            os.path.join(DATAFILES_PATH, 'runset-good', 'bern-2.csv'),
            os.path.join(DATAFILES_PATH, 'runset-good', 'bern-3.csv'),
            os.path.join(DATAFILES_PATH, 'runset-good', 'bern-4.csv'),
            ]
        self.assertEqual(4, runset.chains)
        retcodes = runset._retcodes
        for i in range(len(retcodes)):
            runset._set_retcode(i, 0)
        self.assertTrue(runset._check_retcodes())

        fit = CmdStanMCMC(runset)
        fit._validate_csv_files()
        self.assertEqual(100, fit.draws)
        self.assertEqual(8, len(fit.column_names))
        self.assertEqual('lp__', fit.column_names[0])

        drawset = fit.get_drawset()
        self.assertEqual(
            drawset.shape,
            (fit.runset.chains * fit.draws, len(fit.column_names))
        )
        _ = fit.summary()
        self.assertTrue(True)

        # TODO - use cmdstan test files instead
        expected = '\n'.join(
            [
                'Checking sampler transitions treedepth.',
                'Treedepth satisfactory for all transitions.',
                '\nChecking sampler transitions for divergences.',
                'No divergent transitions found.',
                '\nChecking E-BFMI - sampler transitions HMC potential energy.',
                'E-BFMI satisfactory for all transitions.',
                '\nEffective sample size satisfactory.',
            ]
        )
        self.assertIn(expected, fit.diagnose().replace('\r\n', '\n'))

    def test_validate_big_run(self):
        exe = os.path.join(
            DATAFILES_PATH, 'bernoulli' + EXTENSION
        )
        sampler_args = SamplerArgs()
        cmdstan_args = CmdStanArgs(
            model_name='bernoulli',
            model_exe=exe,
            chain_ids=[1, 2],
            seed=12345,
            output_dir=DATAFILES_PATH,
            method_args=sampler_args,
        )
        runset = RunSet(args=cmdstan_args, chains=2)
        runset._csv_files = [
            os.path.join(DATAFILES_PATH, 'runset-big', 'output_icar_nyc-1.csv'),
            os.path.join(DATAFILES_PATH, 'runset-big', 'output_icar_nyc-1.csv'),
            ]
        fit = CmdStanMCMC(runset)
        fit._validate_csv_files()
        sampler_state = [
            'lp__',
            'accept_stat__',
            'stepsize__',
            'treedepth__',
            'n_leapfrog__',
            'divergent__',
            'energy__',
        ]
        phis = ['phi.{}'.format(str(x + 1)) for x in range(2095)]
        column_names = sampler_state + phis
        self.assertEqual(fit.columns, len(column_names))
        self.assertEqual(fit.column_names, tuple(column_names))
        self.assertEqual(fit.metric_type, 'diag_e')
        self.assertEqual(fit.stepsize.shape, (2,))
        self.assertEqual(fit.metric.shape, (2, 2095))
        self.assertEqual((1000, 2, 2102), fit.sample.shape)
        phis = fit.get_drawset(params=['phi'])
        self.assertEqual((2000, 2095), phis.shape)
        phi1 = fit.get_drawset(params=['phi.1'])
        self.assertEqual((2000, 1), phi1.shape)
        mo_phis = fit.get_drawset(params=['phi.1', 'phi.10', 'phi.100'])
        self.assertEqual((2000, 3), mo_phis.shape)
        phi2095 = fit.get_drawset(params=['phi.2095'])
        self.assertEqual((2000, 1), phi2095.shape)
        with self.assertRaises(Exception):
            fit.get_drawset(params=['phi.2096'])
        with self.assertRaises(Exception):
            fit.get_drawset(params=['ph'])

    # pylint: disable=no-self-use
    def test_custom_metric(self):
        stan = os.path.join(DATAFILES_PATH, 'bernoulli.stan')
        jdata = os.path.join(DATAFILES_PATH, 'bernoulli.data.json')
        bern_model = CmdStanModel(stan_file=stan)
        jmetric = os.path.join(DATAFILES_PATH, 'bernoulli.metric.json')
        # just test that it runs without error
        bern_model.sample(
            data=jdata, chains=4, cores=2, seed=12345, iter_sampling=200,
            metric=jmetric,
        )

    def test_save_csv(self):
        stan = os.path.join(DATAFILES_PATH, 'bernoulli.stan')
        jdata = os.path.join(DATAFILES_PATH, 'bernoulli.data.json')
        bern_model = CmdStanModel(stan_file=stan)
        bern_fit = bern_model.sample(
            data=jdata, chains=4, cores=2, seed=12345, iter_sampling=200
        )
        for i in range(bern_fit.runset.chains):
            csv_file = bern_fit.runset.csv_files[i]
            stdout_file = bern_fit.runset.stdout_files[i]
            self.assertTrue(os.path.exists(csv_file))
            self.assertTrue(os.path.exists(stdout_file))

        # save files to good dir
        bern_fit.save_csvfiles(dir=DATAFILES_PATH)
        for i in range(bern_fit.runset.chains):
            csv_file = bern_fit.runset.csv_files[i]
            self.assertTrue(os.path.exists(csv_file))
        with self.assertRaisesRegex(Exception, 'file exists'):
            bern_fit.save_csvfiles(dir=DATAFILES_PATH)

        tmp2_dir = os.path.join(HERE, 'tmp2')
        os.mkdir(tmp2_dir)
        bern_fit.save_csvfiles(dir=tmp2_dir)
        for i in range(bern_fit.runset.chains):
            csv_file = bern_fit.runset.csv_files[i]
            self.assertTrue(os.path.exists(csv_file))
        for i in range(bern_fit.runset.chains):  # cleanup datafile_path dir
            os.remove(bern_fit.runset.csv_files[i])
            if os.path.exists(bern_fit.runset.stdout_files[i]):
                os.remove(bern_fit.runset.stdout_files[i])
            if os.path.exists(bern_fit.runset.stderr_files[i]):
                os.remove(bern_fit.runset.stderr_files[i])
        shutil.rmtree(tmp2_dir, ignore_errors=True)

        # regenerate to tmpdir, save to good dir
        bern_fit = bern_model.sample(
            data=jdata, chains=4, cores=2, seed=12345, iter_sampling=200
        )
        bern_fit.save_csvfiles()  # default dir
        for i in range(bern_fit.runset.chains):
            csv_file = bern_fit.runset.csv_files[i]
            self.assertTrue(os.path.exists(csv_file))
        for i in range(bern_fit.runset.chains):  # cleanup default dir
            os.remove(bern_fit.runset.csv_files[i])
            if os.path.exists(bern_fit.runset.stdout_files[i]):
                os.remove(bern_fit.runset.stdout_files[i])
            if os.path.exists(bern_fit.runset.stderr_files[i]):
                os.remove(bern_fit.runset.stderr_files[i])

    def test_diagnose_divergences(self):
        exe = os.path.join(
            DATAFILES_PATH, 'bernoulli' + EXTENSION
        )
        sampler_args = SamplerArgs()
        cmdstan_args = CmdStanArgs(
            model_name='bernoulli',
            model_exe=exe,
            chain_ids=[1],
            output_dir=DATAFILES_PATH,
            method_args=sampler_args,
        )
        runset = RunSet(args=cmdstan_args, chains=1)
        runset._csv_files = [
            os.path.join(DATAFILES_PATH, 'diagnose-good',
                             'corr_gauss_depth8-1.csv'),
            ]
        fit = CmdStanMCMC(runset)
        # TODO - use cmdstan test files instead
        expected = '\n'.join(
            [
                'Checking sampler transitions treedepth.',
                '424 of 1000 (42%) transitions hit the maximum '
                'treedepth limit of 8, or 2^8 leapfrog steps.',
                'Trajectories that are prematurely terminated '
                'due to this limit will result in slow exploration.',
                'For optimal performance, increase this limit.',
            ]
        )
        self.assertIn(expected, fit.diagnose().replace('\r\n', '\n'))

    def test_validate_bad_run(self):
        exe = os.path.join(DATAFILES_PATH, 'bernoulli' + EXTENSION)
        jdata = os.path.join(DATAFILES_PATH, 'bernoulli.data.json')
        sampler_args = SamplerArgs(
            iter_sampling=100, max_treedepth=11, adapt_delta=0.95
        )

        # some chains had errors
        cmdstan_args = CmdStanArgs(
            model_name='bernoulli',
            model_exe=exe,
            chain_ids=[1, 2, 3, 4],
            seed=12345,
            data=jdata,
            output_dir=DATAFILES_PATH,
            method_args=sampler_args,
        )
        runset = RunSet(args=cmdstan_args, chains=4)
        for i in range(4):
            runset._set_retcode(i, 0)
        self.assertTrue(runset._check_retcodes())

        # errors reported
        runset._stderr_files = [
            os.path.join(DATAFILES_PATH, 'runset-bad',
                             'bad-transcript-bern-1.txt'),
            os.path.join(DATAFILES_PATH, 'runset-bad',
                             'bad-transcript-bern-2.txt'),
            os.path.join(DATAFILES_PATH, 'runset-bad',
                             'bad-transcript-bern-3.txt'),
            os.path.join(DATAFILES_PATH, 'runset-bad',
                             'bad-transcript-bern-4.txt'),
            ]
        self.assertEqual(len(runset._get_err_msgs()), 4)

        # csv file headers inconsistent
        runset._csv_files = [
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-hdr-bern-1.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-hdr-bern-2.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-hdr-bern-3.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-hdr-bern-4.csv'),
            ]
        fit = CmdStanMCMC(runset)
        with self.assertRaisesRegex(ValueError, 'header mismatch'):
            fit._validate_csv_files()

        # bad draws
        runset._csv_files = [
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-draws-bern-1.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-draws-bern-2.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-draws-bern-3.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-draws-bern-4.csv'),
            ]
        fit = CmdStanMCMC(runset)
        with self.assertRaisesRegex(ValueError, 'draws'):
            fit._validate_csv_files()

        # mismatch - column headers, draws
        runset._csv_files = [
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-cols-bern-1.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-cols-bern-2.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-cols-bern-3.csv'),
            os.path.join(DATAFILES_PATH, 'runset-bad', 'bad-cols-bern-4.csv'),
            ]
        fit = CmdStanMCMC(runset)
        with self.assertRaisesRegex(ValueError, 'bad draw'):
            fit._validate_csv_files()


if __name__ == '__main__':
    unittest.main()

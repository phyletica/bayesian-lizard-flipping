#! /usr/bin/env python

"""
A basic demonstration of Bayesian statistics by flipping lizards.
"""

import sys
import os
import math
import argparse
import unittest
from scipy.stats import beta, binom


class BinomialModel(object):
    """
    A class for demonstrating Bayesian statistics with a binomial sampling
    distribution and a conjugate beta prior.

    Inspired by the lizard-flipping example in Chapter 2 of Luke Harmon's book
    on phylogenetic comparative methods:
    
    https://lukejharmon.github.io/pcm/chapter2_stats/

    >>> m = BinomialModel(100, 10, 0.1)
    >>> m.n
    100
    >>> m.k
    10
    >>> m.p
    0.1
    >>> abs(m.get_likelihood() - 0.1318653) < 0.00001
    True
    >>> abs(m.get_posterior_density() - 13.3184) < 0.0001
    True
    >>> abs(m.get_marginal_likelihood() - 0.00990099) < 0.000001
    True
    """

    def __init__(self,
            number_of_flips = 100,
            number_of_heads = 63,
            probability_of_heads = 0.5,
            prior_beta_a = 1.0,
            prior_beta_b = 1.0):

        self.n = number_of_flips
        self.k = number_of_heads
        self.beta_a = prior_beta_a
        self.beta_b = prior_beta_b
        self.p = probability_of_heads

    def get_prior_distribution(self):
        return beta(self.beta_a, self.beta_b)

    def get_posterior_distribution(self):
        return beta(
                self.beta_a + self.k,
                self.beta_b + (self.n - self.k))
    
    def get_prior_density(self, p = None):
        if p is None:
            p = self.p
        prior_dist = self.get_prior_distribution()
        return prior_dist.pdf(p)

    def get_log_prior_density(self, p = None):
        if p is None:
            p = self.p
        prior_dist = self.get_prior_distribution()
        return prior_dist.logpdf(p)

    def get_posterior_density(self, p = None):
        if p is None:
            p = self.p
        post_dist = self.get_posterior_distribution()
        return post_dist.pdf(p)

    def get_log_posterior_density(self, p = None):
        if p is None:
            p = self.p
        post_dist = self.get_posterior_distribution()
        return post_dist.logpdf(p)

    def get_likelihood(self, p = None):
        if p is None:
            p = self.p
        return binom.pmf(k = self.k, n = self.n, p = p)

    def get_log_likelihood(self, p = None):
        if p is None:
            p = self.p
        return binom.logpmf(k = self.k, n = self.n, p = p)

    def get_log_marginal_likelihood(self):
        """
        To get this, we just have to rearrange Bayes rule as follows:

        p(rate_of_heads | data) = p(data | rate_of_heads) p(rate_of_heads)
                                  ----------------------------------------
                                                 p(data)

        p(data) p(rate_of_heads | data) = p(data | rate_of_heads) p(rate_of_heads)

        p(data) = p(data | rate_of_heads) p(rate_of_heads)
                  ----------------------------------------
                          p(rate_of_heads | data)

        Or in words, the marginal probability of the data equals the likelihood
        times the prior density  divided by the posterior density.

        On a log scale, this is the log likelihood plus the log prior density
        minus the posterior density.
        """
        return (self.get_log_likelihood() + self.get_log_prior_density() -
                self.get_log_posterior_density())

    def get_marginal_likelihood(self):
        return math.exp(self.get_log_marginal_likelihood())


def arg_is_positive_int(i):
    try:
        if int(i) < 1:
            raise
    except:
        msg = '{0!r} is not a positive integer'.format(i)
        raise argparse.ArgumentTypeError(msg)
    return int(i)

def arg_is_positive_float(i):
    try:
        if float(i) <= 0.0:
            raise
    except:
        msg = '{0!r} is not a positive real number'.format(i)
        raise argparse.ArgumentTypeError(msg)
    return float(i)

def arg_is_nonnegative_float(i):
    try:
        if float(i) < 0.0:
            raise
    except:
        msg = '{0!r} is not a non-negative real number'.format(i)
        raise argparse.ArgumentTypeError(msg)
    return float(i)


def main_cli(argv = sys.argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('-n', '--number-of-flips',
            action = 'store',
            type = arg_is_positive_int,
            default = 100,
            help = 'Number of lizard flips.')
    parser.add_argument('-k', '--number-of-heads',
            action = 'store',
            type = arg_is_positive_int,
            default = 63,
            help = 'Number of lizards that land heads up.')
    parser.add_argument('-p', '--probability-of-heads',
            action = 'store',
            type = arg_is_nonnegative_float,
            default = 0.5,
            help = ('Probability of any lizard landing heads up under the '
                    '\'null\' model.'))
    parser.add_argument('-a', '--beta-prior-alpha',
            action = 'store',
            type = arg_is_positive_float,
            default = 1.0,
            help = ('Value of the alpha parameter of the beta prior on the '
                    'probability of heads.'))
    parser.add_argument('-b', '--beta-prior-beta',
            action = 'store',
            type = arg_is_positive_float,
            default = 1.0,
            help = ('Value of the beta parameter of the beta prior on the '
                    'probability of heads.'))

    if argv == sys.argv:
        args = parser.parse_args()
    else:
        args = parser.parse_args(argv)

    m = BinomialModel(
            number_of_flips = args.number_of_flips,
            number_of_heads = args.number_of_heads,
            probability_of_heads = args.probability_of_heads,
            prior_beta_a = args.beta_prior_alpha,
            prior_beta_b = args.beta_prior_beta)

    p = args.probability_of_heads
    msg = """
Let's use Bayes rule to calculate the posterior probability of 2 models:

1.  A "null" model where the probability of heads is fixed to 0.5

2.  An alternative model where the probabiliy of heads is free to vary between
    0 and 1 according to a beta prior

First, we need the marginal probability of the data (the marginal likelihood)
under both models. For the null model there are no free parameters to marginalize
over, so the marginal likelihood is just the likelihood.

    p(data | null model) = {p_data_given_null_model}

For the alternative model, we can easily get the densities from the prior and
posterior disributions (they are both beta distributions), and the likelihood
is a binomial, just like for the null model. With these three numbers, we can
solve for the marginal probability of the data (the denominator of the model's
posterior density).

    p(data | alt model) = {p_data_given_alt_model}

Now, we can get the overall (marginal) probability of the data under either of these two models:

    p(data) = [ p(data | null model) p(null model) ] + [ p(data | alt model) p(alt model) ]

Let's assume a priori that both models are equally probable (i.e, p(null model)
= p(alt model) = 0.5). This simplifies the above equation to:
       
    p(data) = 0.5 p(data | null model) + 0.5 p(data | alt model)

            = 0.5 [ p(data | null model) + p(data | alt model) ]

Now, we can calculate the posterior probability of both models:

    p(null model | data) = p(data | null model) p(null model)
                           ----------------------------------
                                         p(data)

            =              p(data | null model) 0.5
              --------------------------------------------------
              0.5 [ p(data | null model) + p(data | alt model) ]

            =              p(data | null model)
              --------------------------------------------------
                  p(data | null model) + p(data | alt model)

            = {p_null_given_data}

    p(alt model | data) =            p(data | alt model)
                          ------------------------------------------
                          p(data | null model) + p(data | alt model)

            = {p_alt_given_data}
""".format(
        p_data_given_null_model = m.get_likelihood(p),
        p_data_given_alt_model = m.get_marginal_likelihood(),
        p_null_given_data = m.get_likelihood(p) / (m.get_likelihood(p) + m.get_marginal_likelihood()),
        p_alt_given_data = m.get_marginal_likelihood() / (m.get_likelihood(p) + m.get_marginal_likelihood()))

    print(msg)


if __name__ == "__main__":
    if "--run-tests" in sys.argv:

        sys.stderr.write("""
*********************************************************************
Running test suite using the following Python executable and version:
{0}
{1}
*********************************************************************
\n""".format(sys.executable, sys.version))

        import doctest

        # doctest.testmod(verbose = True)
        suite = unittest.TestSuite()
        suite.addTest(doctest.DocTestSuite())

        tests = unittest.defaultTestLoader.loadTestsFromName(
               os.path.splitext(os.path.basename(__file__))[0])
        suite.addTests(tests)

        runner = unittest.TextTestRunner(verbosity = 2)
        runner.run(suite)

        sys.exit(0)

    main_cli()

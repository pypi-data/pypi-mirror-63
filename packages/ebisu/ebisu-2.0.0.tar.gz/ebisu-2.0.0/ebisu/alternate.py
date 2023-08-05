# -*- coding: utf-8 -*-

from .ebisu import _meanVarToBeta
import numpy as np


def _logsubexp(a, b):
  """Evaluate `log(exp(a) - exp(b))` preserving accuracy.

  Subtract log-domain numbers and return in the log-domain.
  Wraps `scipy.special.logsumexp`.
  """
  from scipy.special import logsumexp
  return logsumexp([a, b], b=[1, -1])


def predictRecallMode(prior, tnow):
  """Mode of the immediate recall probability.

  Same arguments as `ebisu.predictRecall`, see that docstring for details. A
  returned value of 0 or 1 may indicate divergence.
  """
  # [1] Mathematica: `Solve[ D[p**((a-t)/t) * (1-p**(1/t))**(b-1), p] == 0, p]`
  alpha, beta, t = prior
  dt = tnow / t
  pr = lambda p: p**((alpha - dt) / dt) * (1 - p**(1 / dt))**(beta - 1)

  # See [1]. The actual mode is `modeBase ** dt`, but since `modeBase` might
  # be negative or otherwise invalid, check it.
  modeBase = (alpha - dt) / (alpha + beta - dt - 1)
  if modeBase >= 0 and modeBase <= 1:
    # Still need to confirm this is not a minimum (anti-mode). Do this with a
    # coarse check of other points likely to be the mode.
    mode = modeBase**dt
    modePr = pr(mode)

    eps = 1e-3
    others = [
        eps, mode - eps if mode > eps else mode / 2, mode + eps if mode < 1 - eps else
        (1 + mode) / 2, 1 - eps
    ]
    otherPr = map(pr, others)
    if max(otherPr) <= modePr:
      return mode
  # If anti-mode detected, that means one of the edges is the mode, likely
  # caused by a very large or very small `dt`. Just use `dt` to guess which
  # extreme it was pushed to. If `dt` == 1.0, and we get to this point, likely
  # we have malformed alpha/beta (i.e., <1)
  return 0.5 if dt == 1. else (0. if dt > 1 else 1.)


def predictRecallMedian(prior, tnow, percentile=0.5):
  """Median (or percentile) of the immediate recall probability.

  Same arguments as `ebisu.predictRecall`, see that docstring for details.

  An extra keyword argument, `percentile`, is a float between 0 and 1, and
  specifies the percentile rather than 50% (median).
  """
  # [1] `Integrate[p**((a-t)/t) * (1-p**(1/t))**(b-1) / t / Beta[a,b], p]`
  # and see "Alternate form assuming a, b, p, and t are positive".
  from scipy.special import betaincinv
  alpha, beta, t = prior
  dt = tnow / t
  return betaincinv(alpha, beta, percentile)**dt


def predictRecallMonteCarlo(prior, tnow, N=1000 * 1000):
  """Monte Carlo simulation of the immediate recall probability.

  Same arguments as `ebisu.predictRecall`, see that docstring for details. An
  extra keyword argument, `N`, specifies the number of samples to draw.

  This function returns a dict containing the mean, variance, median, and mode
  of the current recall probability.
  """
  import scipy.stats as stats
  alpha, beta, t = prior
  tPrior = stats.beta.rvs(alpha, beta, size=N)
  tnowPrior = tPrior**(tnow / t)
  freqs, bins = np.histogram(tnowPrior, 'auto')
  bincenters = bins[:-1] + np.diff(bins) / 2
  return dict(
      mean=np.mean(tnowPrior),
      median=np.median(tnowPrior),
      mode=bincenters[freqs.argmax()],
      var=np.var(tnowPrior))
def updateRecallMonteCarlo(prior, k, n, tnow, tback=None, N=10 * 1000 * 1000):
  """Update recall probability with quiz result via Monte Carlo simulation.

  Same arguments as `ebisu.updateRecall`, see that docstring for details.

  An extra keyword argument `N` specifies the number of samples to draw.
  """
  # [bernoulliLikelihood] https://en.wikipedia.org/w/index.php?title=Bernoulli_distribution&oldid=769806318#Properties_of_the_Bernoulli_Distribution, third equation
  # [weightedMean] https://en.wikipedia.org/w/index.php?title=Weighted_arithmetic_mean&oldid=770608018#Mathematical_definition
  # [weightedVar] https://en.wikipedia.org/w/index.php?title=Weighted_arithmetic_mean&oldid=770608018#Weighted_sample_variance
  import scipy.stats as stats
  from scipy.special import binom
  if tback is None:
    tback = tnow

  alpha, beta, t = prior

  tPrior = stats.beta.rvs(alpha, beta, size=N)
  tnowPrior = tPrior**(tnow / t)

  # This is the Bernoulli likelihood [bernoulliLikelihood]
  weights = binom(n, k) * (tnowPrior)**k * ((1 - tnowPrior)**(n - k))

  # Now propagate this posterior to the tback
  tbackPrior = tPrior**(tback / t)

  # See [weightedMean]
  weightedMean = np.sum(weights * tbackPrior) / np.sum(weights)
  # See [weightedVar]
  weightedVar = np.sum(weights * (tbackPrior - weightedMean)**2) / np.sum(weights)

  newAlpha, newBeta = _meanVarToBeta(weightedMean, weightedVar)

  return newAlpha, newBeta, tback

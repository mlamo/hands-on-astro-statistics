import numpy as np
import time

from scipy.optimize import minimize_scalar
from scipy.special import erf
from scipy.stats import truncnorm
from tqdm import tqdm


# Decorator: display run time of function
def functime(func):
    def exec_func(*args, **kwargs):
        start = time.perf_counter()
        f = func(*args, **kwargs)
        end = time.perf_counter()
        if 'quiet' not in kwargs.keys() or not kwargs['quiet']: 
            print(f"Executed in {1000*(end-start):.2f} milliseconds")
        return f
    return exec_func


def generate_component(mu, pdf, fluctuate=True, **kwargs):
    n = np.random.poisson(lam=mu) if fluctuate else int(mu)
    return pdf.rvs(size=n, **kwargs)


def generate_dataset(mu_signal, mu_background, signal_pdf, background_pdf, fluctuate_signal=True, **kwargs):
    signal = generate_component(mu_signal, signal_pdf, fluctuate=fluctuate_signal, **kwargs)
    background = generate_component(mu_background, background_pdf)
    return np.concatenate((signal, background)), len(signal), len(background)


def loglikelihood(data, mu_signal, mu_background, signal_pdf, background_pdf, **kwargs):
    l1 = mu_signal * signal_pdf.pdf(data, **kwargs) + mu_background * background_pdf.pdf(data)
    return np.log(l1).sum() - (mu_signal + mu_background)


def likelihood_fit(data, mu_background, signal_pdf, background_pdf):
    if len(data)==0: return 0,0
    l1 = minimize_scalar(lambda mu: -loglikelihood(data, mu, mu_background, signal_pdf, background_pdf), bounds=(0, len(data))) 
    return l1.x, -l1.fun # best-fit expected number of signal events and associated log(L) value


def compute_Lambda(data, mu_background, signal_pdf, background_pdf):
    if len(data) == 0: return 0
    loglike_H1 = likelihood_fit(data, mu_background, signal_pdf, background_pdf)[1]
    return 2*(loglike_H1 - loglikelihood(data, 0, mu_background, signal_pdf, background_pdf))


def compute_lambdamu(data, mu, mu_background, signal_pdf, background_pdf):
    if len(data) == 0: return 0
    loglike_H1 = likelihood_fit(data, mu_background, signal_pdf, background_pdf)[1]
    ts = 2*(loglike_H1 - loglikelihood(data, mu, mu_background, signal_pdf, background_pdf))
    return ts


def get_Lambda_distribution(mu_signal, mu_background, signal_pdf, background_pdf, Npseudo_experiments = 10000, fluctuate_signal=True):
    Lambda_table = np.zeros(Npseudo_experiments)
    for i in tqdm(range(Npseudo_experiments)):
        data, _, _ = generate_dataset(mu_signal, mu_background, signal_pdf, background_pdf, fluctuate_signal=fluctuate_signal)
        Lambda_table[i] = compute_Lambda(data, mu_background, signal_pdf, background_pdf)
    return Lambda_table


def get_lambdamu_distribution(mu, mu_signal, mu_background, signal_pdf, background_pdf, Npseudo_experiments = 10000, fluctuate_signal=True):
    Lambda_table = np.zeros(Npseudo_experiments)
    for i in tqdm(range(Npseudo_experiments)):
        data, _, _ = generate_dataset(mu_signal, mu_background, signal_pdf, background_pdf, fluctuate_signal=fluctuate_signal)
        Lambda_table[i] = compute_lambdamu(data, mu, mu_background, signal_pdf, background_pdf)
    return Lambda_table
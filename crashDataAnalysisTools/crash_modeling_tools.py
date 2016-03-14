import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf


def compute_spf(nb_model,predictors):
    # compute the safety performance function
    spf = nb_model.predict(predictors)

    return spf

def compute_eb_weights(nb_model,predictors,segment_lengths):
    # the nb variance is mu+alpha*mu^2 where alpha=1/scale param of the nb distr
    # extract the scale param and get alpha
    alpha = 1/nb_model.scale

    # compute the safety performance function
    spf = compute_spf(nb_model,predictors)
    #spf = nb_model.predict(predictors)

    # compute the weight factor
    # w_i 1/(1+spf_i/(alpha*L_i^gamma)), take gamma=1
    w = 1/(1+(spf/(alpha*segment_lengths)))

    # return the weights
    return w

def estimate_empirical_bayes(nb_model, predictors, segment_lengths, observed_crash_ct):
    # compute the vector of weights
    w = compute_eb_weights(nb_model,predictors,segment_lengths)

    # compute the safety performance function
    spf = compute_spf(nb_model,predictors)

    # compute the safety (i.e., expected crash count at each site as weighted
    # sum of predicted and observed crash count)
    pi = (w*spf) + (1-w)*observed_crash_ct

    # convert to a data frame
    pi = pd.DataFrame(pi,columns=['Safety'])

    # return the vector of safety values
    return pi

def calc_accid_reduc_potential(nb_model, predictors, segment_lengths, observed_crash_ct):
    # compute the vector of weights
    w = compute_eb_weights(nb_model,predictors,segment_lengths)

    # compute the safety performance function
    spf = compute_spf(nb_model,predictors)

    # compute the accident reduction potential
    arp = (1-w)*(observed_crash_ct-spf)

    # convert to a dataframe
    arp = pd.DataFrame(arp,columns=['ARP'])

    return arp

def calc_var_eta_hat(model,data):
    # note data is the design matrix

    # make a vector of zeros to store the output
    var_eta_hat = np.zeros([data.shape[0],1])

    # get the variance-covariance matrix, convert from pd dataframe to np matrix
    cov_mat = model.normalized_cov_params.as_matrix()

    # add a column of 1's to the design matrix for beta_0
    data.insert(0,'intercept',1)

    # loop through the upper right half of the cov mat
    for i in range(0,len(model.params)):
        for j in range(0,i+1):
            # variance term
            if (i==j):
                var_eta_hat = var_eta_hat +  cov_mat[i,j]
                *(data[[i]].as_matrix()**2)
            else: #covariance term
                var_eta_hat = var_eta_hat + cov_mat[i,j]*2
                *data[[i]].as_matrix()*data[[j]].as_matrix()

    return var_eta_hat

def calc_ci_mu:
    return

def calc_pi_m:
    return

def calc_pi_y:
    return

def plot_all_intervals:
    return

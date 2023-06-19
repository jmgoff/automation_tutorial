import numpy as np

# summary of what Latin Hypercube Sampling does
#  1) Divide each parameter range into equally spaced intervals, i
#  2) Sample one point from each interval, n_samples times, such that no two points share the same row or column (n_samples,i)

def latin_hypercube_sample(variable_ranges_dict, variable_types_dict, num_samples,seed=48291):
    np.random.seed(seed)
    variable_ranges = [tuple(v) for v in list(variable_ranges_dict.values())]
    variable_types = [typ for typ in list(variable_types_dict.values())]
    num_variables = len(variable_ranges)
    varseeds = np.random.randint(0,10000,num_variables)
    samples_per_variable = num_samples // num_variables
    #samples_per_variable = 1
    print (samples_per_variable,num_samples)
    # Generate the initial Latin Hypercube
    lhs_matrix = np.zeros((num_samples, num_variables))
    for i in range(num_variables):
        np.random.seed(varseeds[i])
        vtyp = variable_types[i]
        if vtyp == float:
            lhs_matrix[:, i] = np.random.uniform(min(variable_ranges[i]), max(variable_ranges[i]), num_samples)
        elif vtyp == int:
            vrange = list(range(min(variable_ranges[i]),max(variable_ranges[i]) +1,1))
            lhs_matrix[:, i] = np.random.choice(vrange,size=num_samples)
        elif vtyp == str:
            lhs_matrix[:, i] = np.random.choice(variable_ranges[i],size=num_samples)
        else:
            raise TypeError("variable type not implemented")

    # Shuffle the samples within each variable column
    for i in range(num_variables):
        np.random.shuffle(lhs_matrix[:, i])
    # Randomly select one sample from each column to form the final Latin Hypercube
    lhs_samples = np.zeros((num_samples, num_variables))
    for i in range(num_variables):
        lhs_samples[0 :num_samples , i] = lhs_matrix[0 :num_samples , i]
    
    return lhs_samples

# Example usage
#variable_ranges = [(0, 1), (0, 1), (0, 1)]  # Specify the ranges for each variable
#num_samples = 10  # Number of samples to generate
#lhs_samples = latin_hypercube_sample(variable_ranges, num_samples)

# merged_academic = merged DataFrame
# description = label for the independent variable
# selection_column = column where the labels of the independent variables are
# selection_column = values for the independent variable

def bar_graph(merged_academic,selection_column,indepent_var_label):
    import matplotlib.pyplot as plt
    from scipy import stats
    description_list = merged_academic[selection_column].unique()
    merged_academic.loc[:,:] = merged_academic.groupby(['School District Code',selection_column]).mean().reset_index()
    for description in description_list:
        instruction_df = merged_academic.loc[(merged_academic[selection_column] == description)]
        instruction_df.drop_duplicates()
        z = (stats.zscore(instruction_df.loc[:,indepent_var_label]))
        instruction_df.loc[:,(f'{description}_zscore')] = z
        instruction_df = instruction_df.loc[(instruction_df[f'{description}_zscore']<3) & (instruction_df[f'{description}_zscore']>-3)]
        x_values = instruction_df[indepent_var_label]
        y_values = instruction_df['Percent']
        plt.figure(figsize=(15,15), dpi=300)
        plt.scatter(x_values,y_values)
        (slope, intercept, rvalue, pvalue, stderr) = stats.linregress(x_values, y_values)
        print(intercept)
        regress_values = x_values * slope + intercept
        line_eq = "y = " + str(round(slope,2)) + "x +" + str(round(intercept,2))
        plt.xlabel(f"{description}")
        plt.ylabel('% of Graduates into College')
        plt.title(f"{description} vs. Into College ")
        plt.plot(x_values,regress_values,"r-")
        plt.annotate(line_eq,(20,15),fontsize=15,color="red")
        print(f"The r-value is: {rvalue**2}")
        print(f"The intercept value is: {intercept}")
        print(f"The p-value is: {pvalue}")
        plt.savefig(f'../images/{description}.png',bbox_inches = 'tight')
        plt.show()
        
def analysis(df, ind_label,ind_value):
    import matplotlib.pyplot as plt
    from scipy import stats

    grouped = df.groupby(['School District Code', ind_label]).mean().reset_index()
    ind_var_list = grouped[ind_label].unique()
    for ind_var in ind_var_list:
        ind_df = grouped.loc[grouped[ind_label] == ind_var]
        if ind_df[ind_value].mean()==0:
            continue
        ind_df = ind_df.assign(z_score = stats.zscore(ind_df[ind_value]))
        ind_df = ind_df.loc[(ind_df['z_score']<3) & (ind_df['z_score']>-3)]
        x_values = ind_df[ind_value]
        y_values = ind_df['Percent']
        (slope, intercept, rvalue, pvalue, stderr) = stats.linregress(x_values, y_values)
        regress_values = x_values * slope + intercept
        print(f'regression function = f(x) = x*{slope.round(2)} + {intercept.round(2)}')
        print(f'p-value: {pvalue}')
        print(f'std error: {stderr}')
        ind_df.plot.scatter(x = ind_value, y = 'Percent', figsize = (8,8))
        plt.plot(x_values, regress_values, color = 'red')
        plt.title(f'{ind_var} vs college enrollment')
        plt.xlabel(ind_var)
        plt.ylabel('College Enrollment Percentage')
        ind_var = ind_var.replace("/", "&")
        plt.savefig(f'../images/{ind_var}.png')
        plt.show()
                
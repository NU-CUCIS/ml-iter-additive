# ml-iter-additive
This software provides the code for an iterative machine learning framework that uses extremely randomized trees (also known as extreme random forests) for predicting temperature profiles in an additive manufacturing process. 

<p align="center">
  <img src="iterative_additive.png" width="800">
</p>

Requirements:

* Scikit-Learn 0.19.1
* Numpy 1.14
* Pandas 0.22
* XGBoost 0.7 or higher

## Files

#### Core Files
- additive_util.py: Core utility file for this repository (including incorporating neighbor information) 


#### Notebooks
- predict_cube.ipynb
- predict_date_cube.ipynb
- predict_cube_iterative.ipynb

## Data 

The prepared dataset is available at https://www.dropbox.com/s/cbwyhy18ofw0t7j/data.zip?dl=0

## Citation

If you use this code or data, please cite:

A. Paul, M.Mozaffar, Z. Yang, W. Liao, A. Choudhary, J. Cao and A. Agrawal. A real-time iterative approach for temperature profile prediction in additive manufacturing processes. 6th IEEE International Conference on Data Science and Advanced Analytics (DSAA), 2019


## Developer Team & Collaborators 

The code was developed by the <a href="http://cucis.ece.northwestern.edu/">CUCIS</a> group at the Electrical and Computer Engineering Department in Northwestern University. 

1. Arindam Paul (arindam.paul@eecs.northwestern.edu)
2. Jagat Sesh Challa (jagatsesh@northwestern.edu)
3. Ankit Agrawal (ankitag@eecs.northwestern.edu)
4. Wei-keng Liao (wkliao@eecs.northwestern.edu)
5. Alok Choudhary (choudhar@eecs.northwestern.edu)

The development team would like thank the collaborators <a href="https://www.linkedin.com/in/mojtaba-mozaffar-08b95b106/">Mojtaba Mozaffar</a> and <a href="http://ampl.mech.northwestern.edu/faculty/jian-cao/index.html">Prof. Jian Cao </a> from Northwestern's <a href="http://ampl.mech.northwestern.edu/">Advanced Manufacturing Processes Laboratory</a>. 


## Questions/Comments

email: arindam.paul@eecs.northwestern.edu or ankitag@eecs.northwestern.edu</br>
Copyright (C) 2019, Northwestern University.<br/>
See COPYRIGHT notice in top-level directory.

## Funding Support

This work was performed under the following financial assistance award 70NANB19H005 from U.S. Department of Commerce, National Institute of Standards and Technology as part of the Center for Hierarchical Materials Design (CHiMaD). Partial support is also acknowledged from DOE awards DE-SC0014330, DE-SC0019358.

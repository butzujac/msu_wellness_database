### Prerequisites
- anaconda prompt - miniconda install instructions
 https://www.anaconda.com/docs/getting-started/miniconda/install
once intsalled on windows or mac, you should be able to go to the anaconda prompt 
### Installation 
1. open an anaconda prompt
2. clone the repo:
	`git clone https://github.com/github_username/repo_name.git`
3. navigate to the repository: 
	`cd msu_wellness_database`
4. copy the demo_universities.csv file from ms teams in the /datafiles folder into the /data folder. to figure out where the repository is on your computer: 
	use: `cd` on windows or: `pwd` on macOS/Linux
5. create the environment from the environment.yml file:
	`conda env create -f environment.yml`
6. activate the environment:
	`conda activate msu_wd_env`
7. navigate to the example directory where the demo is located:
	`cd examples`
8. open a jupyter notebook on your default browser:
	`jupyter notebook`
9. once you are in juypter, you should see the demo.ipynb file, click on the file:
![[Pasted image 20250308001839.png]]
10. inside the file, click anywhere in the first cell, and press `shift`, then `enter` on your keyboard. This will run script. it may take about 5 minutes, but once it is done you will see an example database table downloaded in the `\example` folder. you can open the table with excel on your machine. 
11. (to be added later) after table has been generated for all universities, push the csv file into github repository where the streamlit website will be hosted from. after implemented, community partners can simply go to the website created to view the final product with cleaner formatting/extra features at any time!
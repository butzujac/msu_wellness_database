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
4. create the environment from the environment.yml file:
	`conda env create -f environment.yml`
5. activate the environment:
	`conda activate msu_wd_env`
6. navigate to the example directory where the demo is located:
	`cd examples`
7. open a jupyter notebook on your default browser:
	`jupyter notebook`
8. once you are in juypter, you should see the demo.ipynb file, click on the file:
![image](https://github.com/user-attachments/assets/bb48511b-0f7b-4c21-9535-386f6d461c7f)

9. inside the file, click anywhere in the first cell, and press `shift`, then `enter` on your keyboard. This will run script. it may take about 5 minutes. to save the sample csv to your computer, do the same proscess for the second cell. 
10. (to be added later) after table has been generated for all universities, push the csv file into github repository where the streamlit website will be hosted from. after implemented, community partners can simply go to the website created to view the final product with cleaner formatting/extra features at any time!

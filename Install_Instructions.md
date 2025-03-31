### Prerequisites
- anaconda prompt - anaconda install instructions
 https://www.anaconda.com/docs/getting-started/anaconda/install
once intsalled on windows or mac, you should be able to go to the anaconda prompt on windows. On mac, make sure you can go to anaconda navigator before opening terminal

### Installation 
1. open an anaconda prompt (or terminal on mac)
2. clone the repo:
   `git clone https://github.com/butzujac/msu_wellness_database.git`
   
4. navigate to the repository: 
	`cd msu_wellness_database`
5. create the environment from the environment.yml file:
	`conda env create -f environment.yml`
6. activate the environment:
	`conda activate msu_wd_env`
7. navigate to the example directory where the demo is located:
	`cd examples`
8. download jupyter for use in the environment:
   	`conda install -n msu_wd_env jupyter`
9. open a jupyter notebook on your default browser:
	`jupyter notebook`
10. once you are in juypter, you should see the demo.ipynb file, click on the file:
![image](https://github.com/user-attachments/assets/bb48511b-0f7b-4c21-9535-386f6d461c7f)

11. inside the file, click anywhere in the first cell, and press `shift`, then `enter` on your keyboard. This will run script. it may take about 5 minutes. to save the sample csv to your computer, do the same proscess for the second cell. 
12. (to be added later) after table has been generated for all universities, push the csv file into github repository where the streamlit website will be hosted from. after implemented, community partners can simply go to the website created to view the final product with cleaner formatting/extra features at any time!

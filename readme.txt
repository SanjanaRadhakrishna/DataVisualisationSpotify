Steps to run our application:

Make sure you have a python interpreter above 3.8

Install all these packages

pip3 install streamlit

pip3 install pandas

pip3 install plotly

pip3 install wordcloud

pip3 install matplotlib


Follow these steps to run the application:

Step 1: Edit this file: $HOME/.streamlit/config.toml

Step 2: Copy the content in config.toml to the above file [This sets our UI color configuration]

Step 3: streamlit cache clear   [This command clears the cache in streamline library]

Step 4: streamlit run wordCloud.py [This command generates our word cloud image]

Step 5: Save the image generated above in the following directory and use this image name: 
	
        figures/wordCloud.png

Step 6: streamlit run main.py  [This command opens our dashboard]
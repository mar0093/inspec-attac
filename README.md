# Running the Script

To run the script the, best way to do it is to use bash and the 'new.sh' script.

Run command 

'''
cd /*location you save the folder*
sh new.sh
'''

This will execute the script below:

```
#!/bin/bash
docker build -t inspec-attac .
docker run --name james-demo -v $PWD/static:/usr/src/app/static -it inspec-attac
```

The first line will build an image with the requirements to run the script. 

(The script normal takes 6-7 minutes to pull required libraries).

The second will build a new container based on the image and will initiate the script to run.

### Rerun script 

To rerun the script execute the 'rerun.sh' with the following command

`sh rerun.sh`

# Notes

The script does not have anny error handling, but as the script runs you will be prompted 3 seperate times. 
1. A URL
2. Column rank(s) to be plotted
3. Column rank to label ticker.

The default input I have used is the url 

'https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population'

With column rank

'4'

and ticker label

'1'

You should then find your new chart under static/ folder
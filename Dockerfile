# start by pulling the python image
FROM python:3.8-alpine


# upgrade pip to the latest version
RUN pip install --upgrade pip

# switch working directory
WORKDIR /LecturerAssistant

# copy every content from the local file to the image
COPY . /LecturerAssistant

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# run website
CMD [ "python", "exe.py" ]

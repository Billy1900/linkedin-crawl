# 1. Requirements
## 1.1 ChromeDriver
Install it on this [website](https://sites.google.com/chromium.org/driver/) and put it in the directory `bin/`. You have to choose different version which is compatible with your operating system (Mac, windows, Linux). 

And then make your chromedriver verified doing the following steps:
  - open terminal
  - Navigate to path where your chromedriver file is located
  - Execute `xattr -d com.apple.quarantine chromedriver`

Example:
```shell
$ cd $(Pkg_Path)/Crawl/bin 
$ xattr -d com.apple.quarantine chromedriver
```

## 1.2 Login Information complement
Due to the limitation, you have to put your user information in `UserInfo.py` file including `username` and `password`.

## 1.3 Others
The rest package requirements are written in the `requirement.txt` file.

# 2. How to use?
Function: crawl the profile page including name, college, location, description, experience, education.

Shellscript like the following:
`python3 main.py`

## TempUpload

A Upload Server For temporary use mostly helpful in ctfs etc.


## Features

- Works Fine on Both Windows and Linux.
- `localhost/list' => List all Files in Working Directory
- `localhost/upload' => Upload using Browser
- Only Uploading is implemented Directory listing is disabled 
- ['.py,'.ipynb'] are blacklisted can be changed in code.


## Uploading Using CLI

###Linux
- Using Curl
```shell
curl -F filename=@LinEnum_report 10.10.14.23:8080
```


###Windows Powershell
- Uploading via powershell depends on powershell version, check powershell.txt for more commands
- I would Strongly recommend using curl.exe `https://curl.se/download.html`
```shell
$Uri = 'http://localhost:8080/'
$Form = @{
    filename     = Get-Item -Path 'c:\Pictures\jdoe.png'
}
$Result = Invoke-WebRequest -Uri $Uri -Method Post -Form $Form
```

### Usage
```shell
$ python upserver.py -h
usage: upserver.py [-h] [-p PORT] [-d DIRECTORY]

A Simple http server to upload for temporary use

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to use avoid using 80,443 for non root user
  -d DIRECTORY, --directory DIRECTORY
                        Working Directory

```


## Built With

* [Python3]

### License

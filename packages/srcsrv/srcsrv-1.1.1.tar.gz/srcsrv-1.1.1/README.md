# Source Indexing  

# Disclaimer  
The author of this package does not warrant the functions contained in the program will meet your requirements or that the operation of the program will be uninterrupted or error-free.  Note: In no event will the author be liable to you for any damages, including any corruption of binaries or PDBs, lost profit, lost savings, lost patience or other incidental or consequential damage.  

With that part out of the way, my goal is to make something that is useful. If you'd like to request additional features, report bugs or provide any other feedback, feel free to reach me.  
[Uri Mann](mailto:abba.mann@gmail.com)  

# Package Description  
Python script to add source indexing to **.PDB** files. The source will be automatically pulled from Git or SubVersion. The python script can be invoked on each **.PDB** file after the link phase of the build is completed. Alternatively, the script can receive a list of one or more directories where the **.PDBs** are placed at the end of the build. Internally, the script simply scans each directory recursively and invoke itself on each file with **.pdb** extension. The script takes the following arguments:

>**-p**, **--pdb** - Path to .PDB file to process *(e.g.: -p c:\path\file.pdb)*. (see also: **--pdbs** option).  
>**-P**, **--pdbs** - One or more directories containing **.PDB** files *(e.g.: --pdbs dir1 dir2 ...)*. The script will recurs to each sub-directory under the specified list. The path is assumed to be fully-qualified or relative to **--build-base**.  
>**-b**, **--build-base** - Root of the build directory. This path correspond with top of the repository branch being built.  
>**-r**, **--branch** - Remote repository branch.  
>**-j**, **--project'** - Repository project (location of cached source). This optional argument will be set to the same value as **--branch** by default.  
>**-x**, **--extensions** - Semicolon separated list of source extensions (default:cpp;c;h).  
>**-s**, **--srcsrv** - Path to SDK or DDK source indexing directory. Default path is **C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\srcsrv** (Windows 8.0 DTfW or newer required).  
>**-c**, **--scheme** - Repository server scheme. Default scheme is *https://*  
>**-u**, **--plugin** - Plugin class. default is srcsrv.plugins.Git. Plugin classes available in current version: **srcsrv.plugins.Git**, **srcsrv.plugins.SVN**.  
>**-c**, **--scheme** - Repository server scheme (default: 'https://).  

Build diagnostic options

>**-o**, **--output** - Path of the source indexing file used for the *srcsrv* stream in the **.PDB**. If this parameter is not used if **--pdbs** option is present. The script will use a file with the same name as the binary with .ini extension *(i.e.: prog.exe will produce prog.pdb which is embedded with prog.ini)*. For build troubleshooting you can use the **--pdb** option without specifying **--output** file. The content of this file is sent to *stdout* and the **.PDB** will not be modified (see: **--no-process**).  
>**-k**, **--keep** - Be default the file specified by the **--output** parameter (or .ini file) is deleted after processing. With this option specified the file is kept in the same directory as the **.PDB**.  
>**-n**, **--no-process** - The script is run without modifying the **.PDB**. Should be used with with **--keep** option or with logging enabled.  
>**-l**, **--log** - Path to log file. By default all logging is visible in *stdout*.

Git options

>**-I**, **--uri** - Git repository server URI. default github.com  
>**-X**, **--hexsha** - Provide repository hash instead of querying Git for hash of the build.  

Git environment  
**GITHUB_TOKEN** - User [token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) This is expected to be the string similar to *1BC49375F092ADAA9DD7B7680190A6D6@*. It is important to include @ as part of the token variable.  
**GITHUB_CREDS** - User credentials. This is expected to be the string: **-u *user:password***  
Note: Only one of the above variables should be set. Not both.  
For indexing, [Git command line tools](https://git-scm.com/downloads) are required to be installed and added to the path.  
For debugging, [cURL command line](https://curl.haxx.se/download.html) tool must be installed and added to the path.  

SubVersion options

>**-I**, **--uri** - SubVersion repository server URI.  
>**-R**, **--revision** - Repository revision instead of querying SVN revision of the build.  

SVN environment  
**SUBVERION_TOKEN** - User credentials. This is expected to be the string similar to *0C0C0D2F04B2B3EF5EF7B6AA252E8679@*. It is important to include @ as part of the token variable  
**SUBVERION_CREDS** - User credentials. This is expected to be the string: **-u *user:password***  
Note: Only one of the above variables should be set. Not both.  
For indexing, [SubVersion command line tools](https://subversion.apache.org/packages.html) are required to be installed and added to the path.  
For debugging, [cURL command line](https://curl.haxx.se/download.html) tool must be installed and added to the path.  

Note: Credentials for secured access must be set in order to allow the debugger to automatically download the indexed source. **GITHUB_TOKEN** or **SVN_CREDS** can be set as an environment variable or in [srcsrv.ini](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/the-srcsrv-ini-file) file.  

The script can also be invoked with a response file. Using **@path\resp_file_name**. The file can contain any of the above parameters. Response file and command line parameters can be combined. Example:

```
--build-base D:\dev\svn\myproject
--uri mysubversion.com
--pdbs debug release amd64dbg amd64rel  
--branch myrepo/myproj/trunk
--project myrepo/myproj
--log ..\srcsrv.log
--plugin srcsrv.plugins.SVN
```

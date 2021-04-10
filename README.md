# iTerm2 Cryto ticker

Cryto ticker for your iterm status bar. Backed by ethereumdb. Supports multiple coins and currencies.

![screenshot](https://user-images.githubusercontent.com/15212758/114254794-7561f500-9966-11eb-90a3-8e4bf579294d.png)



# Setup

These instructions are provided for convenience. 
For more information see the [iterm2 documentation](https://iterm2.com/python-api/tutorial/index.html#tutorial-index).


## Installing the script

Open iTerm2. In the menu, click **Scripts** > **Manage** > **New Python Script**

When prompted, select **Full Environment** then select **Long-Running Daemon**

Specify the **Save As** name `cryptoticker` and **PyPI Dependencies** as `aiohttp`. `aiodns` is optional, but recommended. 

If you haven't downloaded a python runtime for iTerm, you'll be prompted to do so.

Copy the cryptoticker.py to the iterm environment:  
```  
cp ./cryptoticker.py ~/Library/Application Support/iTerm2/Scripts/cryptoticker/cryptoticker/cryptoticker.py  
```  
Move cryptoticker into the AutoLaunch folder (create this directory if it does not exist)  
```  
mv ~/Library/Application Support/iTerm2/Scripts/cryptoticker ~/Library/Application Support/iTerm2/Scripts/AutoLaunch/cryptoticker
```

## Configure the status bar


1. If you haven't already, enable the status bar:  
Go to **Preferences** > **Profiles** > **Session**. Turn on **Status bar enabled**.
2. To add the ticker component, click **Configure Status Bar**. Drag the cryto ticker component into the 
active components area.
3. Click on the component then **Configure Component**. Here you can enable specific data for the coin.

![config](https://user-images.githubusercontent.com/15212758/114254807-90cd0000-9966-11eb-86ac-baccf89b3060.png)

You can also configure by `ctrl+click`ing on the status bar itself.

![quickconfig](https://user-images.githubusercontent.com/15212758/114254794-7561f500-9966-11eb-90a3-8e4bf579294d.png)

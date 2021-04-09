# iTerm2 Cryto ticker

Cryto ticker for your iterm status bar

![screenshot](https://user-images.githubusercontent.com/15212758/114246667-07a6d080-9948-11eb-934b-45889d111089.png)



# Setup

These instructions are provided for convenience. 
For more information see the [iterm2 documentation](https://iterm2.com/documentation-status-bar.html).


## Installing the script

1. Open iTerm2. In the menu, click **Scripts** > **Manage** > **New Python Script**
2. When prompted, select **Full Environment** then select **Long-Running Daemon**
3. Specify the **Save As** name `cryptoticker` and **PyPI Dependencies** as `aiohttp`. If you haven't downloaded a python runtime for iTerm, you'll be prompted to do so.
4. Copy the cryptoticker.py to the iterm environment:  
`cp ./cryptoticker.py ~/Library/Application Support/iTerm2/Scripts/cryptoticker/cryptoticker/cryptoticker.py`
5. Move cryptoticker into the AutoLaunch folder (create this directory if it does not exist)  
`mv ~/Library/Application Support/iTerm2/Scripts/cryptoticker ~/Library/Application Support/iTerm2/Scripts/AutoLaunch/cryptoticker`

## Configure the status bar


1. If you haven't already, enable the status bar:  
Go to **Preferences** > **Profiles** > **Session**. Turn on **Status bar enabled**.
2. To add the ticker component, click **Configure Status Bar**. Drag the cryto ticker component into the 
active components area.
3. Click on the component then **Configure Component**. Here you can enable/disable specific coins or specific data. 
By default, all coins are enabled and only price is shown.

![config](https://user-images.githubusercontent.com/15212758/114246735-33c25180-9948-11eb-85a9-d7b3771e65f7.png)

You can also configure by `ctrl+click`ing on the status bar itself.

![quickconfig](https://user-images.githubusercontent.com/15212758/114246701-1f7e5480-9948-11eb-8cce-e8367d100e19.png)

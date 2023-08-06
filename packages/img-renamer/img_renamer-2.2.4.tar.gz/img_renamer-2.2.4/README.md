# Image renamer

## Description

**img_rename** is a Python script to rename images in numberic order.


## Usage

### Rename with CLI

This will rename all images in `~/Pictures` folder like this: `0000001.png`, `0000002.png`, `0000003.png`...
```
img_renamer ~/Pictures
```

### Rename non-interactively / automatic yes to prompts

This will rename all images in `~/Pictures` folder without asking anything. It will still show list what is being renamed
```
img_renamer -y ~/Pictures
```

### Print help text

Simply run this
```
img_renamer --help
```

## Author
[Miika Launiainen](https://gitlab.com/miicat)

## License

This library is licensed under GPLv3

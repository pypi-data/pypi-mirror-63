# Trellogy

<br>

<blockquote>Trello handling module via Trello REST API</blockquote>

<br>

Trellogy is a handy tool to communicate with [Trello](https://trello.com) board. It relies on the REST API provided by the Trello team, but this is not the official wrapper of Trello API.

Trello cards, lists, and attachments are implemented as classes in this module. Every component inherits API metadata to its subclasses and make things much more convenient. This project is open-ended, and bug / issue reports are always appreciated.


<br>

## Why I made it

I made it for fun, frankly speaking. Most of my programs are invented from a escape of repeating tedious tasks over and over. Although there is a fancy tool called Butler,  it wasn't suitable for my picky needs of creating sophisticated cards and labels with extremely specific details. Hence, I quickly jotted down some codes that can act as a bottom-line material of other Trello-related projects.

<br>

## Installation

You can install trellogy via PIP:

```
pip install trellogy
```

Or perhaps on Linux:

```
sudo pip3 install trellogy
```

<br>


## Quick Example

Here is a quick example to show what Trellogy looks like.

```python
from trellogy import Trellogy

trello = Trellogy(key=TRELLO_API_KEY,
                  token=TRELLO_API_TOKEN,
                  board_id=BOARD_ID,
                  trash_id=TRASH_BOARD_ID)

for trello_list in trello.get_lists():
    cards = trello_list.cards
    for card in cards:
        print(card.name)
        print(card.desc)
```


<br>

## Code Explanation

### Import Trellogy

```
from trellogy import Trellogy
```

<br>

### Initialize Trellogy


```python
trello = Trellogy(key=TRELLO_API_KEY,
                  token=TRELLO_API_TOKEN,
                  board_id=BOARD_ID,
                  trash_id=TRASH_BOARD_ID)
```

In order to initialize, Trello receives 3 mandatory arguments and 1 optional argument. The descriptions are as follows:

<br>

#### mandatory: key, token, board_id

In order to use the Trello REST API, you need to get a `key` and a `token`. You can grab yours from [here](https://trello.com/app-key). `board_id` is the ID of the board you want to manage. One way to figure out your ID of the board is to put **.json** at the end of the URL. For example, suppose your board URL is https://trello.com/b/SAMPLE/BOARD. You jump to https://trello.com/b/SAMPLE/BOARD.json, and will see your board ID at the top of the textlines.

<br>

#### optional: trash_id

Unfortunately, there is no way you can get rid of a card or a list via API directly - you can only archive it. So as a workaround, you can create a junk board and toast all the nasty stuff into it - *just like how you use the trash bin inside your laptop*. `trash_id` is the board ID of that junk board. You may leave it empty if you don't need the workaround.

<br>

### Trellogy.List

```python
trello_lists = trello.get_lists()
for trello_list in trello_lists:
    cards = trello_list_list.cards
```

`get_lists()` method will return a list of **&lt;Trellogy.List&gt;**. Each class own various methods and properties including `cards`, a list of **&lt;Trellogy.Card&gt;** classes.

<br>

### Trellogy.Card

```python
for card in cards:
    print(card.name)
    print(card.desc)
```

**&lt;Trellogy.Card&gt;** class is the implementation of Trello card. It contains read-only properties including name, desc, etc. Please note that updating each property is possible only by using `update(**kwargs)` method.


For more detail, take a look at the [Trellogy Documentation](https://github.com/ChiantiScarlett/trellogy/blob/master/doc/README.md).


<br>


## Special thanks to

- My coffee cup
- Various musicians that I seek on Youtube every day

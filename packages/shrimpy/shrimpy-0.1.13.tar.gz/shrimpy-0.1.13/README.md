# :fried_shrimp: shrimpy

A minimal engine for choose-your-own-adventure games.

## Install

Installing shrimpy is easy. To install shrimpy on your computer, open your terminal and enter:

`sudo pip3 install shrimpy`

## About

In shrimpy, **a game is simply a folder that contains scene files.** Scene files are written in JSON.

## Create

To create your first shrimpy game, make a new folder somewhere on your computer. Name your new folder `hello-shrimpy`.

Next, create a new file called `start.json` inside `hello-shrimpy`. Copy the following code into `start.json`:

````
{
  "id": "start",
  "text": "You lose!",
  "options": [
    {
      "text": "What? Already?",
      "scene": "end"
    }
  ]
}
````

Once you have saved `start.json` inside of the `hello-shrimpy` folder, create a second file in `hello-shrimpy` and name it `end.json`. Copy the following code into `end.json`:

````
{
  "id": "end",
  "text": "GAME OVER. Enter q to quit.",
  "options": [
    {
      "text": "(play again)",
      "scene": ""
    }
  ]
}
````

At this point, you should have a folder called `hello-shrimpy` that contains two files: `start.json` and `end.json`.

That's it! Your new shrimpy game is finished and ready to play.

## Play

To play the game you just created, navigate into the `hello-shrimpy` folder and run:

`shrimpy play`

## Quit

To quit playing a shrimpy game, you can always enter `q` when prompted for an option number.

## Update

Shrimpy keeps getting better. To update shrimpy to the latest version, enter:

`sudo pip3 install shrimpy -U`

## Uninstall

Down with shrimpy! To uninstall shrimpy from your computer, enter:

`sudo pip3 uninstall shrimpy`

## Scene Schema

For your reference, the following JSON schema is used to validate scene files:

 ````
 {
 	"$schema": "http://json-schema.org/draft-04/schema#",
 	"type": "object",
 	"properties": {
 		"id": {
 			"type": "string"
 		},
 		"text": {
 			"type": "string"
 		},
 		"options": {
 			"type": "array",
 			"items": [
 				{
 					"type": "object",
 					"properties": {
 						"text": {
 							"type": "string"
 						},
 						"scene": {
 							"type": "string"
 						}
 					},
 					"required": [
 						"text",
 						"scene"
 					]
 				}
 			]
 		}
 	},
 	"required": [
 		"id",
 		"text",
 		"options"
 	]
 }
 ````
To learn more about JSON Schema, [click here](https://json-schema.org/).

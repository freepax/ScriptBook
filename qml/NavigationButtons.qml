import Qt 4.7


Rectangle {
    id: buttonBox
    property color textColor: "white"

    signal buttonClicked(int button)

    Row {
        PushButton { /// Gets you back to all the documents
            id: documentButton
            text: "Docs"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(0)
        }

        PushButton { /// Gets you back to the books in the opened document
            id: bookButton
            text: "Books"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(1)
        }

        PushButton { /// Gets you back to the chapter in the book
            id: chapterButton
            text: "Chapt"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(2)
        }

        PushButton { /// Show more options
            id: settingsButton
            text: "Tools"; textColor: buttonBox.textColor
            height: button_height(); width: button_width(); radius: 4
            onTrigger: buttonBox.buttonClicked(3)
        }
    }
}

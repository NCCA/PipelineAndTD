import QtQuick 2.0
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3
Window {
    width: 400
    height: 300
    visible: true
    title: qsTr("Menus")
    ColumnLayout
    {
        anchors.fill: parent

        spacing: 3
    Button {
        Layout.alignment: Qt.AlignLeft
        id : menubutton
        text : "menu"
        onPressed: {
                contextMenu.popup()
        }

        Action{
            id :  saveAction
            onTriggered : {
            menubutton.text = "Save Pressed"
            }
        }
        Action{
            id :  saveAsAction
            onTriggered : {
            menubutton.text = "Save As Pressed"
            }
        }
        Action{
            id :  newAction
            onTriggered : {
            menubutton.text = "New Pressed"
            }
        }

        Menu {
            id: contextMenu
            MenuItem {
                text: "Save"
                action: saveAction
            }
            MenuItem {
                text: "Save As"
                action: saveAsAction
            }
            MenuItem {
                text: "New"
                action: newAction
            }
            MenuSeparator{}
            MenuItem { text: "Export" }
            MenuItem { text: "Export As" }
            MenuSeparator{}
            Menu{
                id : submenu
                MenuItem{text :"Sub"}
                MenuItem{text :"Menus"}
                MenuItem{text :"Pop Out"}
                MenuItem{text :"But can be difficut"}
                MenuSeparator{}
                Menu {
                    MenuItem{text :"To Navigate"}
                }
            }

        }
    }
    ComboBox {
        Layout.alignment: Qt.AlignLeft
        id: comboBox
        model: ["First", "Second", "Third"]
        onCurrentIndexChanged: {
            combo_result.text = comboBox.textAt(comboBox.currentIndex)
        }
    }
    Text {
        Layout.alignment: Qt.AlignLeft
        id : combo_result
        text : "choose from combo"
    }

    }

}


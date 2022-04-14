import QtQuick
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls.Material 2.12

Window {
    width:  800
    height: 400
    visible: true
    title: qsTr("Text Input")
    color: "lightgrey"
    GridLayout
    {
        anchors.fill: parent
        columns: 8
        rows : 8
        Rectangle {
            id: rectangle
            Layout.row : 0
            Layout.column: 0
            Layout.columnSpan : 4
            Layout.rowSpan: 1

            color: "white"
            TextInput {
                id: simpleEdit
                text: "Text Input"
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.leftMargin: 0
            }
            height: childrenRect.height
            width: childrenRect.width
        }
        Rectangle {
            Layout.row : 1
            Layout.column: 0
            Layout.columnSpan : 4
            Layout.rowSpan: 1

            color: "white"
            TextInput {
                id: password
                text: "Enter a Password"
                horizontalAlignment: Text.AlignRight
                echoMode: TextInput.PasswordEchoOnEdit
                cursorVisible: true
                inputMask: "*****************"

            }
            height: childrenRect.height
            width: childrenRect.width
        }

        Rectangle {
            Layout.row : 2
            Layout.column: 0
            Layout.columnSpan : 8
            Layout.rowSpan: 4

            color: "white"
            TextArea {
                id: textArea
                text: "Enter a Password"
                horizontalAlignment: Text.AlignRight
                cursorVisible: true

            }
            height: childrenRect.height
            width: childrenRect.width
        }


    }

}

import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2

Window {
    visible: true
    width: 800
    height: 600
    title: qsTr("Button Types")
    GridLayout{
        anchors.fill: parent
        rows:   4
        columns:   3
    Button {
        Layout.row : 0
        Layout.columnSpan : 1
        text: qsTr("Simple Button")
        onPressed : {
            button1action.text = "onPress"
        }

        onReleased: {
            button1action.text = "onReleased"
        }

    }
    Text {
        id : button1action
        Layout.row : 0
        Layout.column : 1
        text : ""
    }
    ButtonGroup {
        id: radioGroup
    }
        RadioButton{
            Layout.row : 1
            Layout.column: 0
            checked: true
            text : qsTr("radio buttons")
              ButtonGroup.group: radioGroup
        }
        RadioButton{
            Layout.row : 1
            Layout.column: 1
            checked: false
            text : qsTr("are")
            ButtonGroup.group: radioGroup
        }
        RadioButton{
            Layout.row : 1
            Layout.column: 2

            checked: false
            text : qsTr("exclusive")
            ButtonGroup.group: radioGroup
        }
        CheckBox{
            Layout.row : 2
            Layout.column : 0
            checked : true
            text : qsTr("check box")
        }
        Text{
            Layout.row : 2
            Layout.column: 1
            text : qsTr("This is a Dialog Button Box")
        }
        
        ToolButton{
            Layout.row : 3
            Layout.column: 1
            icon.name: "edit-cut"
            icon.source: "images/ncca.png"
            icon.width: 200
            icon.height: 100
            text : qsTr("Tool Button")
        }
    }


}

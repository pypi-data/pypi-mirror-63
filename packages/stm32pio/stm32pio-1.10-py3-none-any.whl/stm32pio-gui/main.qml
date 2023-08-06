import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtGraphicalEffects 1.12
import QtQuick.Dialogs 1.3 as QtDialogs

import Qt.labs.platform 1.1 as QtLabs

import ProjectListItem 1.0
import Settings 1.0


ApplicationWindow {
    id: mainWindow
    visible: true
    minimumWidth: 980  // comfortable initial size
    minimumHeight: 300
    height: 530
    title: 'stm32pio'
    color: 'whitesmoke'

    /*
       Notify the front-end about the end of an initial loading
    */
    signal backendLoaded()
    onBackendLoaded: loadingOverlay.close()
    Popup {
        id: loadingOverlay
        visible: true
        parent: Overlay.overlay
        anchors.centerIn: Overlay.overlay
        modal: true
        background: Rectangle { opacity: 0.0 }
        closePolicy: Popup.NoAutoClose

        contentItem: Column {
            BusyIndicator {}
            Text { text: 'Loading...' }
        }
    }

    /*
       Slightly customized QSettings
    */
    property Settings settings: appSettings
    QtDialogs.Dialog {
        id: settingsDialog
        title: 'Settings'
        standardButtons: QtDialogs.StandardButton.Save | QtDialogs.StandardButton.Cancel
        GridLayout {
            columns: 2

            Label {
                text: 'Editor'
                Layout.preferredWidth: 140
            }
            TextField {
                id: editor
                text: settings.get('editor')
            }

            Label {
                text: 'Verbose output'
                Layout.preferredWidth: 140
            }
            CheckBox {
                id: verbose
                leftPadding: -3
                checked: settings.get('verbose')
            }
        }
        onAccepted: {
            settings.set('editor', editor.text);
            settings.set('verbose', verbose.checked);
        }
    }

    QtDialogs.Dialog {
        id: aboutDialog
        title: 'About'
        standardButtons: QtDialogs.StandardButton.Close
        ColumnLayout {
            Rectangle {
                width: 250
                height: 100
                TextArea {
                    width: parent.width
                    height: parent.height
                    readOnly: true
                    selectByMouse: true
                    wrapMode: Text.WordWrap
                    textFormat: TextEdit.RichText
                    horizontalAlignment: TextEdit.AlignHCenter
                    verticalAlignment: TextEdit.AlignVCenter
                    text: `2018 - 2020 © ussserrr<br>
                           <a href='https://github.com/ussserrr/stm32pio'>GitHub</a>`
                    onLinkActivated: Qt.openUrlExternally(link)
                    MouseArea {
                        anchors.fill: parent
                        acceptedButtons: Qt.NoButton  // we don't want to eat clicks on the Text
                        cursorShape: parent.hoveredLink ? Qt.PointingHandCursor : Qt.ArrowCursor
                    }
                }
            }
        }
    }

    /*
       Project representation is, in fact, split in two main parts: one in a list and one is an actual workspace.
       To avoid some possible bloopers we should make sure that both of them are loaded before performing
       any actions with the project. To not reveal QML-side implementation details to the backend we define
       this helper function that counts number of widgets currently loaded for each project in model and informs
       the Qt-side right after all necessary components went ready.
    */
    property var initInfo: ({})
    function setInitInfo(projectIndex) {
        if (projectIndex in initInfo) {
            initInfo[projectIndex]++;
        } else {
            initInfo[projectIndex] = 1;
        }

        if (initInfo[projectIndex] === 2) {
            delete initInfo[projectIndex];  // index can be reused
            projectsModel.getProject(projectIndex).qmlLoaded();
        }
    }

    // TODO: fix (jumps skipping next)
    function moveToNextAndRemove() {
        // Select and go to some adjacent index before deleting the current project. -1 is a correct
        // QML index (note that for Python it can jump to the end of the list, ensure a consistency!)
        const indexToRemove = projectsListView.currentIndex;
        let indexToMoveTo;
        if (indexToRemove === (projectsListView.count - 1)) {
            indexToMoveTo = indexToRemove - 1;
        } else {
            indexToMoveTo = indexToRemove + 1;
        }

        projectsListView.currentIndex = indexToMoveTo;
        projectsWorkspaceView.currentIndex = indexToMoveTo;

        projectsModel.removeProject(indexToRemove);
    }

    menuBar: MenuBar {
        Menu {
            title: '&Menu'
            Action { text: '&Settings'; onTriggered: settingsDialog.open() }
            Action { text: '&About'; onTriggered: aboutDialog.open() }
            MenuSeparator { }
            Action { text: '&Quit'; onTriggered: Qt.quit() }
        }
    }

    /*
       All layouts and widgets try to be adaptive to variable parents, siblings, window and whatever else sizes
       so we extensively using Grid, Column and Row layouts. The most high-level one is a composition of the list
       and the workspace in two columns
    */
    GridLayout {
        anchors.fill: parent
        rows: 1
        z: 2  // do not clip glow animation (see below)

        ColumnLayout {
            Layout.preferredWidth: 2.6 * parent.width / 12
            Layout.fillHeight: true

            /*
               The dynamic list of projects (initially loaded from the QSettings, can be modified later)
            */
            ListView {
                id: projectsListView
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true  // crawls under the Add/Remove buttons otherwise

                highlight: Rectangle { color: 'darkseagreen' }
                highlightMoveDuration: 0  // turn off animations
                highlightMoveVelocity: -1

                model: projectsModel  // backend-side
                delegate: Component {
                    /*
                       (See setInitInfo docs) One of the two main widgets representing the project. Use Loader component
                       as it can give us the relible time of all its children loading completion (unlike Component.onCompleted)
                    */
                    Loader {
                        onLoaded: setInitInfo(index)
                        sourceComponent: RowLayout {
                            id: projectsListItem
                            property bool initloading: true  // initial waiting for the backend-side
                            property bool actionRunning: false
                            property ProjectListItem project: projectsModel.getProject(index)
                            Connections {
                                target: project  // (newbie hint) sender
                                // Currently, this event is equivalent to the complete initialization of the backend side of the project
                                onNameChanged: {
                                    initloading = false;
                                }
                                onActionDone: {
                                    actionRunning = false;
                                }
                            }
                            ColumnLayout {
                                Layout.preferredHeight: 50

                                Text {
                                    leftPadding: 5
                                    rightPadding: busy.running ? 0 : leftPadding
                                    Layout.alignment: Qt.AlignBottom
                                    Layout.preferredWidth: busy.running ?
                                                           (projectsListView.width - parent.height - leftPadding) :
                                                           projectsListView.width
                                    elide: Text.ElideMiddle
                                    maximumLineCount: 1
                                    text: `<b>${display.name}</b>`
                                }
                                Text {
                                    leftPadding: 5
                                    rightPadding: busy.running ? 0 : leftPadding
                                    Layout.alignment: Qt.AlignTop
                                    Layout.preferredWidth: busy.running ?
                                                           (projectsListView.width - parent.height - leftPadding) :
                                                           projectsListView.width
                                    elide: Text.ElideRight
                                    maximumLineCount: 1
                                    text: display.current_stage
                                }
                            }

                            BusyIndicator {
                                id: busy
                                Layout.alignment: Qt.AlignVCenter
                                Layout.preferredWidth: parent.height
                                Layout.preferredHeight: parent.height
                                running: projectsListItem.initloading || projectsListItem.actionRunning
                            }

                            MouseArea {
                                x: parent.x
                                y: parent.y
                                width: parent.width
                                height: parent.height
                                enabled: !parent.initloading
                                onClicked: {
                                    projectsListView.currentIndex = index;
                                    projectsWorkspaceView.currentIndex = index;
                                }
                            }
                        }
                    }
                }
            }

            QtLabs.FolderDialog {
                id: addProjectFolderDialog
                currentFolder: QtLabs.StandardPaths.standardLocations(QtLabs.StandardPaths.HomeLocation)[0]
                onAccepted: projectsModel.addProjectByPath(folder)
            }
            RowLayout {
                Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
                Layout.fillWidth: true

                Button {
                    text: 'Add'
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                    display: AbstractButton.TextBesideIcon
                    icon.source: 'icons/add.svg'
                    onClicked: addProjectFolderDialog.open()
                }
                Button {
                    text: 'Remove'
                    Layout.alignment: Qt.AlignVCenter | Qt.AlignHCenter
                    display: AbstractButton.TextBesideIcon
                    icon.source: 'icons/remove.svg'
                    onClicked: moveToNextAndRemove()
                }
            }
        }


        /*
           Main workspace. StackLayout's Repeater component seamlessly uses the same projects model (showing one -
           current - project per screen) so all data is synchronized without any additional effort.
        */
        StackLayout {
            id: projectsWorkspaceView
            Layout.preferredWidth: 9.4 * parent.width / 12
            Layout.fillHeight: true
            Layout.leftMargin: 5
            Layout.rightMargin: 10
            Layout.topMargin: 10
            // clip: true  // do not use as it'll clip glow animation

            Repeater {
                // Use similar to ListView pattern (same projects model, Loader component)
                model: projectsModel
                delegate: Component {
                    Loader {
                        onLoaded: setInitInfo(index)
                        /*
                           Use another one StackLayout to separate Project initialization "screen" and Main one
                        */
                        sourceComponent: StackLayout {
                            id: mainOrInitScreen  // for clarity
                            currentIndex: -1  // at widget creation we do not show main nor init screen

                            Layout.fillWidth: true
                            Layout.fillHeight: true

                            property ProjectListItem project: projectsModel.getProject(index)
                            Connections {
                                target: project  // sender
                                onLogAdded: {
                                    if (level === Logging.WARNING) {
                                        log.append('<font color="goldenrod"><pre style="white-space: pre-wrap">' + message + '</pre></font>');
                                    } else if (level >= Logging.ERROR) {
                                        log.append('<font color="red"><pre style="white-space: pre-wrap">' + message + '</pre></font>');
                                    } else {
                                        log.append('<pre style="white-space: pre-wrap">' + message + '</pre>');
                                    }
                                }
                                // Currently, this event is equivalent to the complete initialization of the backend side of the project
                                onNameChanged: {
                                    for (let i = 0; i < buttonsModel.count; ++i) {
                                        projActionsRow.children[i].enabled = true;
                                    }

                                    const state = project.state;
                                    const completedStages = Object.keys(state).filter(stateName => state[stateName]);
                                    if (completedStages.length === 1 && completedStages[0] === 'EMPTY') {
                                        initScreenLoader.active = true;
                                        mainOrInitScreen.currentIndex = 0;  // show init dialog
                                    } else {
                                        mainOrInitScreen.currentIndex = 1;  // show main view
                                    }
                                }
                            }

                            /*
                               Prompt a user to perform initial setup
                            */
                            Loader {
                                id: initScreenLoader
                                active: false
                                sourceComponent: Column {
                                    Text {
                                        text: "To complete initialization you can provide PlatformIO name of the board"
                                        padding: 10
                                    }
                                    Row {
                                        padding: 10
                                        spacing: 10
                                        ComboBox {
                                            id: board
                                            editable: true
                                            model: boardsModel  // backend-side (simple string model)
                                            textRole: 'display'
                                            onAccepted: {
                                                focus = false;
                                            }
                                            onActivated: {
                                                focus = false;
                                            }
                                            onFocusChanged: {
                                                if (!focus) {
                                                    if (find(editText) === -1) {
                                                        editText = textAt(0);  // should be 'None' at index 0
                                                    }
                                                } else {
                                                    selectAll();
                                                }
                                            }
                                        }
                                        /*
                                           Trigger full run
                                        */
                                        CheckBox {
                                            id: runCheckBox
                                            text: 'Run'
                                            enabled: false
                                            ToolTip {
                                                visible: runCheckBox.hovered
                                                Component.onCompleted: {
                                                    const actions = [];
                                                    for (let i = 3; i < buttonsModel.count; ++i) {
                                                        actions.push(`<b>${buttonsModel.get(i).name}</b>`);
                                                    }
                                                    text = `Do: ${actions.join(' → ')}`;
                                                }
                                            }
                                            Connections {
                                                target: board
                                                onFocusChanged: {
                                                    if (!board.focus) {
                                                        if (board.editText === board.textAt(0)) {  // should be 'None' at index 0
                                                            runCheckBox.checked = false;
                                                            runCheckBox.enabled = false;
                                                        } else {
                                                            runCheckBox.enabled = true;
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                        CheckBox {
                                            id: openEditor
                                            text: 'Open editor'
                                            ToolTip {
                                                text: 'Start the editor specified in the <b>Settings</b> after the completion'
                                                visible: openEditor.hovered
                                            }
                                        }
                                    }
                                    Button {
                                        text: 'OK'
                                        topInset: 15
                                        leftInset: 10
                                        topPadding: 20
                                        leftPadding: 18
                                        onClicked: {
                                            // All operations will be queued
                                            projectsListView.currentItem.item.actionRunning = true;

                                            project.run('save_config', [{
                                                'project': {
                                                    'board': board.editText === board.textAt(0) ? '' : board.editText
                                                }
                                            }]);

                                            if (runCheckBox.checked) {
                                                for (let i = 3; i < buttonsModel.count - 1; ++i) {
                                                    buttonsModel.setProperty(i, 'shouldRunNext', true);
                                                }
                                                projActionsRow.children[3].clicked();
                                            }

                                            if (openEditor.checked) {
                                                if (runCheckBox.checked) {
                                                    buttonsModel.setProperty(buttonsModel.count - 1, 'shouldStartEditor', true);
                                                } else {
                                                    projActionsRow.children[1].clicked();
                                                }
                                            }

                                            mainOrInitScreen.currentIndex = 1;  // go to main screen
                                            initScreenLoader.sourceComponent = undefined;  // destroy init screen
                                        }
                                    }
                                }
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                Layout.fillHeight: true

                                /*
                                   Detect and reflect changes of a project outside of the app
                                */
                                QtDialogs.MessageDialog {
                                    // TODO: case: .ioc file can be removed on init stage too (i.e. when initDialog is active)
                                    id: projectIncorrectDialog
                                    text: `The project was modified outside of the stm32pio and .ioc file is no longer present.<br>
                                           The project will be removed from the app. It will not affect any real content`
                                    icon: QtDialogs.StandardIcon.Critical
                                    onAccepted: {
                                        moveToNextAndRemove();
                                        projActionsButtonGroup.lock = false;
                                    }
                                }

                                /*
                                   Show this or action buttons
                                */
                                Text {
                                    id: initErrorMessage
                                    visible: false
                                    padding: 10
                                    text: "The project cannot be initialized"
                                    color: 'red'
                                }

                                /*
                                   The core widget - a group of buttons mapping all main actions that can be performed on the given project.
                                   They also serve the project state displaying - each button indicates a stage associated with it:
                                    - green: done
                                    - yellow: in progress right now
                                    - red: an error has occured during the last execution
                                */
                                ButtonGroup {
                                    id: projActionsButtonGroup
                                    buttons: projActionsRow.children
                                    signal stateReceived()
                                    signal actionDone(string actionDone, bool success)
                                    property bool lock: false  // TODO: is it necessary? mb make a dialog modal or smth.
                                    onStateReceived: {  // TODO: cache state!
                                        if (mainWindow.active && (index === projectsWorkspaceView.currentIndex) && !lock) {
                                            const state = project.state;
                                            project.stageChanged();

                                            if (state['LOADING']) {
                                                //
                                            } else if (state['INIT_ERROR']) {
                                                projActionsRow.visible = false;
                                                initErrorMessage.visible = true;
                                            } else if (!state['EMPTY']) {
                                                lock = true;  // projectIncorrectDialog.visible is not working correctly (seems like delay or smth.)
                                                projectIncorrectDialog.open();
                                            } else if (state['EMPTY']) {
                                                for (let i = 0; i < buttonsModel.count; ++i) {
                                                    projActionsRow.children[i].palette.button = 'lightgray';
                                                    if (state[buttonsModel.get(i).state]) {
                                                        projActionsRow.children[i].palette.button = 'lightgreen';
                                                    }
                                                }
                                            }
                                        }
                                    }
                                    onActionDone: {
                                        for (let i = 0; i < buttonsModel.count; ++i) {
                                            projActionsRow.children[i].enabled = true;
                                        }
                                    }
                                    onClicked: {
                                        for (let i = 0; i < buttonsModel.count; ++i) {
                                            projActionsRow.children[i].enabled = false;
                                            projActionsRow.children[i].glowVisible = false;
                                        }
                                    }
                                    Component.onCompleted: {
                                        // Several events lead to a single handler:
                                        //  - the state has changed and explicitly informs about it
                                        //  - the project was selected in the list
                                        //  - the app window has got the focus
                                        project.stateChanged.connect(stateReceived);
                                        projectsWorkspaceView.currentIndexChanged.connect(stateReceived);
                                        mainWindow.activeChanged.connect(stateReceived);

                                        project.actionDone.connect(actionDone);
                                    }
                                }
                                RowLayout {
                                    id: projActionsRow
                                    Layout.fillWidth: true
                                    Layout.bottomMargin: 7
                                    z: 1  // for the glowing animation
                                    Repeater {
                                        model: ListModel {
                                            id: buttonsModel
                                            ListElement {
                                                name: 'Clean'
                                                action: 'clean'
                                                shouldStartEditor: false
                                            }
                                            ListElement {
                                                name: 'Open editor'
                                                action: 'start_editor'
                                                margin: 15  // margin to visually separate first 2 actions as they doesn't represent any state
                                            }
                                            ListElement {
                                                name: 'Initialize'
                                                state: 'INITIALIZED'
                                                action: 'save_config'
                                                shouldRunNext: false
                                                shouldStartEditor: false
                                            }
                                            ListElement {
                                                name: 'Generate'
                                                state: 'GENERATED'
                                                action: 'generate_code'
                                                shouldRunNext: false
                                                shouldStartEditor: false
                                            }
                                            ListElement {
                                                name: 'Init PlatformIO'
                                                state: 'PIO_INITIALIZED'
                                                action: 'pio_init'
                                                shouldRunNext: false
                                                shouldStartEditor: false
                                            }
                                            ListElement {
                                                name: 'Patch'
                                                state: 'PATCHED'
                                                action: 'patch'
                                                shouldRunNext: false
                                                shouldStartEditor: false
                                            }
                                            ListElement {
                                                name: 'Build'
                                                state: 'BUILT'
                                                action: 'build'
                                                shouldRunNext: false
                                                shouldStartEditor: false
                                            }
                                        }
                                        delegate: Button {
                                            text: name
                                            Layout.rightMargin: model.margin
                                            enabled: false  // turn on after project initialization
                                            property alias glowVisible: glow.visible
                                            function runOwnAction() {
                                                projectsListView.currentItem.item.actionRunning = true;
                                                palette.button = 'gold';
                                                let args = [];  // JS array cannot be attached to a ListElement (at least in a non-hacky manner)
                                                if (model.action === 'start_editor') {
                                                    args.push(settings.get('editor'));
                                                }
                                                project.run(model.action, args);
                                            }
                                            onClicked: {
                                                runOwnAction();
                                            }
                                            /*
                                               Detect modifier keys:
                                                - Ctrl: start the editor after an operation(s)
                                                - Shift: continuous actions run
                                            */
                                            MouseArea {
                                                anchors.fill: parent
                                                hoverEnabled: true
                                                property bool ctrlPressed: false
                                                property bool ctrlPressedLastState: false
                                                property bool shiftPressed: false
                                                property bool shiftPressedLastState: false
                                                function shiftHandler() {
                                                    for (let i = 2; i <= index; ++i) {  // TODO: magic number, actually...
                                                        if (shiftPressed) {
                                                            projActionsRow.children[i].palette.button = Qt.lighter('lightgreen', 1.2);
                                                        } else {
                                                            projActionsButtonGroup.stateReceived();
                                                        }
                                                    }
                                                }
                                                onClicked: {
                                                    if (ctrlPressed && model.action !== 'start_editor') {
                                                        model.shouldStartEditor = true;
                                                    }
                                                    if (shiftPressed && index >= 2) {
                                                        // run all actions in series
                                                        for (let i = 2; i < index; ++i) {
                                                            buttonsModel.setProperty(i, 'shouldRunNext', true);
                                                        }
                                                        projActionsRow.children[2].clicked();
                                                        return;
                                                    }
                                                    parent.clicked();  // propagateComposedEvents doesn't work...
                                                }
                                                onPositionChanged: {
                                                    ctrlPressed = mouse.modifiers & Qt.ControlModifier;  // bitwise AND
                                                    if (ctrlPressedLastState !== ctrlPressed) {
                                                        ctrlPressedLastState = ctrlPressed;
                                                    }

                                                    shiftPressed = mouse.modifiers & Qt.ShiftModifier;  // bitwise AND
                                                    if (shiftPressedLastState !== shiftPressed) {
                                                        shiftPressedLastState = shiftPressed;
                                                        shiftHandler();
                                                    }
                                                }
                                                onEntered: {
                                                    statusBar.text =
                                                        `<b>Ctrl</b>-click to open the editor specified in the <b>Settings</b> after the operation,
                                                         <b>Shift</b>-click to perform all actions prior this one (including).
                                                         <b>Ctrl</b>-<b>Shift</b>-click for both`;
                                                }
                                                onExited: {
                                                    statusBar.text = '';

                                                    ctrlPressed = false;
                                                    ctrlPressedLastState = false;

                                                    if (shiftPressed || shiftPressedLastState) {
                                                        shiftPressed = false;
                                                        shiftPressedLastState = false;
                                                        shiftHandler();
                                                    }
                                                }
                                            }
                                            Connections {
                                                target: projActionsButtonGroup
                                                onActionDone: {
                                                    if (actionDone === model.action) {
                                                        if (success) {
                                                            glow.color = 'lightgreen';
                                                        } else {
                                                            palette.button = 'lightcoral';
                                                            glow.color = 'lightcoral';
                                                        }
                                                        glow.visible = true;

                                                        if (model.shouldRunNext) {
                                                            model.shouldRunNext = false;
                                                            projActionsRow.children[index + 1].clicked();
                                                        }

                                                        if (model.shouldStartEditor) {
                                                            model.shouldStartEditor = false;
                                                            for (let i = 0; i < buttonsModel.count; ++i) {
                                                                if (buttonsModel.get(i).action === 'start_editor') {
                                                                    // Use runOwnAction for no additional actions in parent handlers
                                                                    projActionsRow.children[i].runOwnAction();
                                                                    break;
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                            /*
                                               Blinky glowing
                                            */
                                            RectangularGlow {
                                                id: glow
                                                visible: false
                                                anchors.fill: parent
                                                cornerRadius: 25
                                                glowRadius: 20
                                                spread: 0.25
                                                onVisibleChanged: {
                                                    visible ? glowAnimation.start() : glowAnimation.complete();
                                                }
                                                SequentialAnimation {
                                                    id: glowAnimation
                                                    loops: 3
                                                    OpacityAnimator {
                                                        target: glow
                                                        from: 0
                                                        to: 1
                                                        duration: 1000
                                                    }
                                                    OpacityAnimator {
                                                        target: glow
                                                        from: 1
                                                        to: 0
                                                        duration: 1000
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }

                                Rectangle {
                                    Layout.fillWidth: true
                                    Layout.fillHeight: true

                                    ScrollView {
                                        anchors.fill: parent
                                        TextArea {
                                            id: log
                                            readOnly: true
                                            selectByMouse: true
                                            wrapMode: Text.WordWrap
                                            font.family: 'Courier'
                                            font.pointSize: 10  // different on different platforms, Qt's bug
                                            textFormat: TextEdit.RichText
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    /*
       Simple text line. Currently, doesn't support smart intrinsic properties as a fully-fledged status bar,
       but is used only for a single feature so not a big deal
    */
    footer: Text {
        id: statusBar
        padding: 10
    }
}

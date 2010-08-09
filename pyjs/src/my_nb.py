from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel

from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.Button import Button
from pyjamas.ui.Label import Label
from pyjamas.ui.HTML import HTML

from pyjamas.ui import KeyboardListener

from pyjamas import Window
from pyjamas import DOM

from pyjamas.JSONService import JSONProxy

class InputArea(TextArea):
    '''
    A box for inputting text, based on Pyjamas' :class:TextArea.
    Its methods mostly exist to make certain operations more convenient,
    in the context of this notebook module.
    '''
    
    def __init__(self):
        '''Constructor: initialize parameters to more appropriate values.'''
        TextArea.__init__(self, StyleName='cell_input')
        self.setVisibleLines(1)
        self.setCharacterWidth(90)

    def adjust_visible_lines(self, extra=0):
        lines = self.getText().split('\n')
        num_lines = len(lines)
        self.setVisibleLines(num_lines + extra)

    def cursor_coordinates(self):
        text = self.getText()
        lines = text.split('\n')
        pos = self.getCursorPos()
        for row, line in enumerate(lines):
            line_len = len(line)
            pos = pos - line_len - 1
            if pos < 0:
                return {'row': row, 'col': pos + line_len + 1}
    
    def get_cell(self):
        return self.getParent().getParent()

class EvalHandler:
    def __init__(self, cell):
        self._cell = cell
    
    def onCompletion(self, text):
        pass
        
    def onError(self, responseText, status):
        Window.alert(responseText)

    
    def onRemoteResponse(self, response, request_info):
        self._cell.set_output(response.strip("'"))
        self._cell._output_panel.setVisible(True)
    
    def onRemoteError(self, code, error_dict, request_info):
        Window.alert(error_dict)

class CellWidget(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self)
        
        self._add_input_panel()
        self._add_button_panel()
        self._add_output_panel()
        self.setStyleName('cell_widget')
    
    def _add_input_panel(self):
        self.input = InputArea()
        self._input_prompt = Label(StyleName='input_prompt')
        self._input_panel = HorizontalPanel()
        self._input_panel.add(self._input_prompt)
        self._input_panel.add(self.input)
        self.add(self._input_panel)
    
    def _add_button_panel(self):
        self._eval_button = Button('Evaluate', getattr(self, 'evaluate'))
        self.button_panel = HorizontalPanel(StyleName='cell_buttons')
        self.button_panel.add(self._eval_button)
        self.button_panel.setVisible(False)
        self.add(self.button_panel)
    
    def _add_output_panel(self):
        self.output = HTML()
        self._output_prompt = Label(StyleName='output_prompt')
        self._output_panel = HorizontalPanel()
        self._output_panel.add(self._output_prompt)
        self._output_panel.add(self.output)
        self._output_panel.setVisible(False)
        self.add(self._output_panel)
    
    def get_data(self):
        return {'input': self.input.getText(), 'output': self.output.getHTML()}
    
    def add_output(self, html):
        self.output.setHTML(self.output.getHTML() + html)
    
    def set_output(self, html):
        self.output.setHTML(html)
    
    def get_text(self):
        return self.input.getText()
    
    def set_text(self, text):
        self.input.setText(text)
    
    def evaluate(self, sender=None):
        data = self.get_text()
        handler = EvalHandler(self)
        #params = [data]
        #service = JSONProxy(url='http://localhost:8686/')
        #service.callMethod('add', params, handler=handler)
        service = JSONProxy(url='/everything/_test')
        service.sendRequest('', data, handler=handler)
    
    def show_buttons(self):
        self.button_panel.setVisible(True)
    
    def hide_buttons(self):
        self.button_panel.setVisible(False)
    
    def set_id(self, name):
        self._input_prompt.setText('In  [%s]: ' % (name,))
        self._output_prompt.setText('Out [%s]: ' % (name,))

class WorksheetWidget(VerticalPanel):
    def __init__(self):
        VerticalPanel.__init__(self)
        self._cell_list = []
        self._current_cell = None
        
        RootPanel().add(self)

    def cell_factory(self):
        return CellWidget()

    def add_cell(self, index=None):
        cw = self.cell_factory()
        cw.button_panel.add(Button('Insert cell', getattr(self, 'insert_cell')))
        cw.input.addFocusListener(self)
        cw.input.addKeyboardListener(self)
        
        if isinstance(index, int):
            self._cell_list.insert(index, cw)
            self.insert(cw, index)
        else:
            self._cell_list.append(cw)
            self.add(cw)
        
        if self._current_cell:
            self._current_cell.hide_buttons()
        self._current_cell = cw
        
        cw.input.setFocus(True)
        
        self.update_cell_indices()
    
    def insert_cell(self, sender):
        self.add_cell(self.current_index() + 1)
    
    def delete_cell(self, index):
        if self.okay_to_delete():
            cell = self._cell_list.pop(index)
            old_text = cell.get_text()
            cell.removeFromParent()
            if index > 0:
                next = self._cell_list[index - 1]
                next.set_text('%s\n%s' % (next.get_text(), old_text))
            else:
                next = self._cell_list[index]
                next.set_text('%s\n%s' % (old_text, next.get_text()))
            
            next.input.adjust_visible_lines()
            next.input.setFocus(True)
            
            self.update_cell_indices()
            self.prevent_default_event() # Don't delete the new last character
    
    def okay_to_delete(self):
        return self.num_cells() > 1
    
    def current_index(self):
        return self._cell_list.index(self._current_cell)
    
    def num_cells(self):
        return len(self._cell_list)
    
    def update_cell_indices(self):
        for i, x in enumerate(self._cell_list):
            x.set_id(i + 1)
    
    def next_cell_up(self):
        index = self.current_index()
        if index > 0:
            above = self._cell_list[index - 1]
            above.input.setFocus(True)
    
    def next_cell_down(self):
        index = self.current_index()
        num_cells = self.num_cells()
        if index < num_cells - 1 and num_cells > 1:
            next = self._cell_list[index + 1]
            next.input.setFocus(True)
    
    def prevent_default_event(self):
        event = DOM.eventGetCurrentEvent()
        if event.preventDefault:
            event.preventDefault()
    
    def onFocus(self, sender):
        if isinstance(sender, InputArea):
            self._current_cell.hide_buttons()
            self._current_cell = sender.get_cell()
            self._current_cell.show_buttons()
    
    def onLostFocus(self, sender):
        pass
    
    def onKeyDown(self, sender, key_code, modifiers):
        if isinstance(sender, InputArea):
            coords = sender.cursor_coordinates()
            if key_code == KeyboardListener.KEY_ENTER and \
                    modifiers == KeyboardListener.MODIFIER_SHIFT:
                sender.get_cell().evaluate()
                self.prevent_default_event() # Don't add a new line
            elif key_code == KeyboardListener.KEY_ENTER:
                sender.adjust_visible_lines(1)
            elif key_code == KeyboardListener.KEY_BACKSPACE and \
                    coords['col'] == 0:
                if coords['row'] == 0: # Merge cells
                    self.delete_cell(self.current_index())
                else: # Just show 1 fewer row
                    sender.adjust_visible_lines(-1)
            elif key_code == KeyboardListener.KEY_UP:
                if coords['row'] == 0:
                    self.prevent_default_event()
                    self.next_cell_up()
            elif key_code == KeyboardListener.KEY_DOWN:
                if coords['row'] == sender.getVisibleLines() - 1:
                    self.prevent_default_event()
                    self.next_cell_down()
            
    def onKeyPress(self, sender, key_code, modifiers):
        pass
    
    def onKeyUp(self, sender, key_code, modifiers):
        pass
    

if __name__ == '__main__':
    w = WorksheetWidget()
    w.add_cell()

from my_nb import CellWidget, WorksheetWidget, EvalHandler

from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.Button import Button
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.HTMLPanel import HTMLPanel
from pyjamas.ui.Label import Label

from pyjamas import Window

from pyjamas.JSONService import JSONProxy

class EvalSaver(EvalHandler):
    def __init__(self, worksheet, cell):
        EvalHandler.__init__(self, cell)
        self._worksheet = worksheet
        self._cell = cell
    
    def onRemoteResponse(self, response, request_info):
        EvalHandler.onRemoteResponse(self, response, request_info)
        self._cell.save(self._worksheet)
        self._worksheet.save()

class PersistentCell(CellWidget):
    def __init__(self, worksheet):
        CellWidget.__init__(self)
        self._db_id = worksheet._next_uuid
        worksheet._generate_uuid()
        self._worksheet = worksheet
        
    def save(self):
        data = self.get_data()
        params = [{'id': self._db_id, 'data': data}]
        service = JSONProxy(url='/json/')
        service.sendRequest('couch_nb.save_cell', params, handler=CellHandler)
    
    def delete(self):
        if self._db_id:
            params = [{'id': self._db_id}]
            service = JSONProxy(url='/json/')
            service.sendRequest('couch_nb.delete_cell', params, handler=CellHandler)
    
    def evaluate(self, sender=None):
        data = self.get_text()
        handler = EvalSaver(self._worksheet, self)
        params = [{'id': self._db_id, 'input': data}]
        service = JSONProxy(url='/json/')
        service.sendRequest('couch_nb.eval_cell', params, handler=handler)
    
class CellHandler:
    def onRemoteResponse(self, response, request_info):
        pass
    
    def onRemoteError(self, code, error_dict, request_info):
        Window.alert(error_dict)

class SaveHandler:
    def onRemoteResponse(self, response, request_info):
        pageloc = Window.getLocation()
        pageloc.setSearchDict({'worksheet': response})
    
    def onRemoteError(self, code, error_dict, request_info):
        Window.alert(error_dict)
    

class WorksheetSaver:
    def __init__(self, worksheet):
        self._worksheet = worksheet
    
    def onRemoteResponse(self, response, request_info):
        pass
    
    def onRemoteError(self, code, error_dict, request_info):
        Window.alert(error_dict)

class GenerateUUID:
    def __init__(self, worksheet):
        self._worksheet = worksheet
    
    def onRemoteResponse(self, response, request_info):
        self._worksheet._next_uuid = response
    
    def onRemoteError(self, code, error_dict, request_info):
        Window.alert(error_dict)

class LockHandler:
    def __init__(self, worksheet):
        self._worksheet = worksheet
    
    def onRemoteResponse(self, response, request_info):
        if response == True:
            self._worksheet.lock_cells()
    
    def onRemoteError(self, code, error_dict, request_info):
        Window.alert(error_dict) 

class PersistentWorksheet(WorksheetWidget):
    def __init__(self):
        self._generate_uuid()
        self.extra_ui_elements()
        
        WorksheetWidget.__init__(self)
        
        self.get_params()
        
        _id = self.get_id_from_params()
        self.set_name(_id)
        self.retrieve_from_db(_id)
    
    def get_params(self):
        pageloc = Window.getLocation()
        self.get_params = pageloc.getSearchDict()
    
    def get_id_from_params(self):
        return self.get_params.get('worksheet', '')
    
    def cells_disabled(self):
        params = [{'id': self.get_name()}]
        service = JSONProxy(url='/json/')
        service.sendRequest('couch_nb.worksheet_locked', params, handler=LockHandler(self))
    
    def lock_cells(self):
        for cell in self._cell_list:
            cell.input.setEnabled(False)
            cell.hide_buttons()
    
    def extra_ui_elements(self):
        self._name = Label(StyleName='heading')
        RootPanel().add(self._name)
    
    def cell_factory(self):
        return PersistentCell(self)
    
    def _generate_uuid(self):
        params = []
        service = JSONProxy(url='/json/')
        service.sendRequest('couch_nb.generate_uuid', params, handler=GenerateUUID(self))
    
    def save_all_to_db(self):
        _id = self.get_name()
        if _id != '':
            cells = [cell.get_data() for cell in self._cell_list]
            params = [{'cells': cells, '_id': _id}]
            service = JSONProxy(url='/json/')
            service.sendRequest('couch_nb.save', params, handler=SaveHandler)
        else:
            Window.alert('Please provide a worksheet name before saving.')
    
    def save(self):
        name = self.get_name()
        params = [{'id': name, 'cells': [c._db_id for c in self._cell_list]}]
        service = JSONProxy(url='/json/')
        service.sendRequest('couch_nb.save_worksheet', params, handler=WorksheetSaver(self))
    
    def retrieve_from_db(self, _id):
        params = [{'name': _id}]
        service = JSONProxy(url='/json/')
        service.sendRequest('couch_nb.retrieve', params, handler=self)
        
    def onRemoteResponse(self, response, request_info):
        if response['cells'] == []:
            self.add_cell()
        else:
            for cell in response['cells']:
                self.fill_cell(cell['id'], cell['input'], cell['output'])
            # Check if worksheet should be in "locked" mode
            self.cells_disabled()

    def onRemoteError(self, code, error_dict, request_info):
        Window.alert(error_dict)
    
    def fill_cell(self, db_id, cell_input, cell_output):
        WorksheetWidget.add_cell(self)
        active = self._current_cell
        active._db_id = db_id
        active.input.setText(cell_input)
        active.input.adjust_visible_lines()
        active.add_output(cell_output)
        active._output_panel.setVisible(True)
    
    def add_cell(self, index=None):
        WorksheetWidget.add_cell(self, index)
        self._current_cell.save()
        self.save()
    
    def delete_cell(self, index):
        if self.okay_to_delete():
            self._cell_list[index].delete()
            WorksheetWidget.delete_cell(self, index)
            self.save()
    
    def set_name(self, name):
        self._name.setText(name)
    
    def get_name(self):
        return self._name.getText()

if __name__ == '__main__':
    w = PersistentWorksheet()
    

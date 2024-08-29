from abc import ABCMeta, abstractstaticmethod
import time
import numpy as np
import copy

from model.segment import segmentAnything

class ICommand(metaclass=ABCMeta):
    """The command interface, which all commands will implement"""

    @abstractstaticmethod
    def execute(*args):
        """The required execute method which all command objects will use"""

class IUndoRedo(metaclass=ABCMeta):
    """The Undo Redo interface"""
    @abstractstaticmethod
    def history():
        """the history of the states"""

    @abstractstaticmethod
    def undo():
        """for undoing the hsitory of the states"""

    @abstractstaticmethod
    def redo():
        """for redoing the hsitory of the states"""

class label(IUndoRedo):
    """The Invoker Class"""

    def __init__(self):
        self._commands = {}
        self._history = [(0.0, [])]  # A default setting of object list
        self._history_position = 0  # The position that is used for UNDO/REDO

    @property
    def history(self):
        """Return all records in the History list"""
        return self._history
    
    @property
    def get_current_data(self):
        """Return current records in the History list"""
        return copy.deepcopy(self._history[self._history_position][1])

    def register(self, command_name, command):
        """All commands are registered in the Invoker Class"""
        self._commands[command_name] = command

    def execute(self, command_name, *args):
        """Execute a pre defined command and log in history"""
        if command_name in self._commands.keys():
            prev_data = copy.deepcopy(self.history[self._history_position][1])
            object_data = self._commands[command_name].execute(prev_data, args)
            self._history_position += 1
            if len(self._history) == self._history_position:
                # This is a new event in hisory
                self._history.append((time.time(), object_data))
            else:
                # This occurs if there was one of more UNDOs and then a new
                # execute command happened. In case of UNDO, the history_position
                # changes, and executing new commands purges any history after
                # the current position"""
                self._history = self._history[:self._history_position]
                self._history.append((time.time(), object_data))
        else:
            print(f"Command [{command_name}] not recognised")

    def undo(self):
        """Undo a command if there is a command that can be undone.
        Update the history position so that further UNDOs or REDOs
        point to the correct index"""
        if self._history_position > 0:
            self._history_position -= 1
        else:
            print("nothing to undo")

    def redo(self):
        """Perform a REDO if the history_position is less than the end of the history list"""
        if self._history_position + 1 < len(self._history):
            self._history_position += 1
        else:
            print("nothing to REDO")

class editor:
    """The Receiver"""
    
    def add_object(self, *args):
        currentData = args[0][0]
        label = args[0][1][0]
        currentData.append({'label': label, 'input_point': [], 'input_label': []})
            
        return currentData
    
    def add_point(self, *args):
        currentData = args[0][0]
        idx = args[0][1][0]
        input_point = args[0][1][1]
        input_label = args[0][1][2]
        mask = args[0][1][3]
        scores = args[0][1][4]
        logits = args[0][1][5]
        
        if idx < len(currentData):
            currentData[idx].update({
                'input_point': input_point,
                'input_label': input_label,
                'mask': mask,
                'scores': scores,
                'logits': logits
            })
        
        else:
            print(f'{idx} is out of range')
        
        return currentData
    
    def exclude_point(self, *args):
        currentData = args[0][0]
            
        return currentData
    
    def reset(self, *args):
        currentData = args[0][0]
        idx = args[0][1][0]
        
        if idx < len(currentData):
            currentData[idx]['input_point'] = []
            currentData[idx]['input_label'] = []
            if 'mask' in currentData[idx]:
                del currentData[idx]['mask']
            if 'scores' in currentData[idx]:
                del currentData[idx]['scores']
            if 'logits' in currentData[idx]:
                del currentData[idx]['logits']
        
        else:
            print(f'{idx} is out of range')
            
        return currentData
        
    def rename(self, *args):
        currentData = args[0][0]
        idx = args[0][1][0]
        newLabel = args[0][1][1]
        
        if idx < len(currentData):
            currentData[idx]['label'] = newLabel
        
        else:
            print(f'{idx} is out of range')
            
        return currentData
        
    def delete(self, *args):
        currentData = args[0][0]
        idx = args[0][1][0]

        if idx < len(currentData):
            del currentData[idx]
        
        else:
            print(f'{idx} is out of range')
            
        return currentData
        
class AddObjectCommand(ICommand):
    """A Command object, which implements the ICommand interface"""
        
    def __init__(self, editor):
        self._editor = editor

    def execute(self, *args):
        newData = self._editor.add_object(args)
        
        return newData
        
class AddPointCommand(ICommand):
    """A Command object, which implements the ICommand interface"""
        
    def __init__(self, editor):
        self._editor = editor

    def execute(self, *args):
        newData = self._editor.add_point(args)
        
        return newData
        
class ExcludePointCommand(ICommand):
    """A Command object, which implements the ICommand interface"""
        
    def __init__(self, editor):
        self._editor = editor

    def execute(self, *args):
        newData = self._editor.exclude_point(args)
        
        return newData
        
class ResetCommand(ICommand):
    """A Command object, which implements the ICommand interface"""
        
    def __init__(self, editor):
        self._editor = editor

    def execute(self, *args):
        newData = self._editor.reset(args)
        
        return newData
        
class RenameCommand(ICommand):
    """A Command object, which implements the ICommand interface"""
        
    def __init__(self, editor):
        self._editor = editor

    def execute(self, *args):
        newData = self._editor.rename(args)
        
        return newData
        
class DeleteCommand(ICommand):
    """A Command object, which implements the ICommand interface"""
        
    def __init__(self, editor):
        self._editor = editor

    def execute(self, *args):
        newData = self._editor.delete(args)
        
        return newData
        
def batch_register(mode):
    # Receiver
    receiver = editor()
    
    # Create Commands
    if mode == 'Manual':
        creat = AddObjectCommand(receiver)
        add = AddPointCommand(receiver)
        exclude = ExcludePointCommand(receiver)
        reset = ResetCommand(receiver)
        rename = RenameCommand(receiver)
        delete = DeleteCommand(receiver)
        
        # Register the commands with the invoker (Switch)
        command = label()
        command.register("create", creat)
        command.register("add", add)
        command.register("exclude", exclude)
        command.register("reset", reset)
        command.register("rename", rename)
        command.register("delete", delete)
    
    return command

class action_manager:
    def __init__(self):
        self.sam = segmentAnything()
        self.whole_list = {'Auto': {}, 'Manual': {}}

    def get_data(self, filename, mode):
        commander = self.whole_list[mode][filename]['editor']
        obj_data = commander.get_current_data
        if len(obj_data) > 0:
            obj_list = [obj['label'] for obj in obj_data]
        
            return obj_list
        
        else:
            return None
        
    def regist_file(self, filename, image, mode):
        if filename in self.whole_list[mode]:
            print(f'{filename}, {mode} is already registered')
            print('load history')
        
        else:
            commander = batch_register(mode)
            if mode == 'Auto':
                result = self.sam.auto_mode(image)
            elif mode == 'Manual':
                result = self.sam.manual_mode(image)
                
            self.whole_list[mode].update({filename: {'editor': commander, 'predictor': result}})
    
    def create_obj(self, filename, objName, mode):
        commander = self.whole_list[mode][filename]['editor']
        commander.execute('create', objName)

    def add_point(self, filename, objIdx, xy_pos, mode):
        commander = self.whole_list[mode][filename]['editor']
        predictor = self.whole_list[mode][filename]['predictor']
        obj_data = commander.get_current_data[objIdx]
        input_point = obj_data['input_point']
        input_point.append(xy_pos)
        input_label = obj_data['input_label']
        input_label.append(1)
        scores = None
        logits = None
        if 'mask' in obj_data:
            scores = obj_data['scores']
            logits = obj_data['logits']
        mask, scores, logits = self.sam.add_point(predictor, input_point, input_label, scores, logits)
        commander.execute('add', objIdx, input_point, input_label, mask, scores, logits)

        return mask

    def exclude_point(self, filename, objIdx, xy_pos, mode):
        commander = self.whole_list[mode][filename]['editor']
        predictor = self.whole_list[mode][filename]['predictor']
        obj_data = commander.get_current_data[objIdx]
        input_point = obj_data['input_point']
        input_point.append(xy_pos)
        input_label = obj_data['input_label']
        input_label.append(0)
        scores = None
        logits = None
        if 'mask' in obj_data:
            scores = obj_data['scores']
            logits = obj_data['logits']
        mask, scores, logits = self.sam.add_point(predictor, input_point, input_label, scores, logits)
        commander.execute('add', objIdx, input_point, input_label, mask, scores, logits)

        return mask
    
# receiver = editor()

# # Create Commands
# creat = AddObjectCommand(receiver)
# add = AddPointCommand(receiver)
# exclude = ExcludePointCommand(receiver)
# reset = ResetCommand(receiver)
# rename = RenameCommand(receiver)
# delete = DeleteCommand(receiver)

# # Register the commands with the invoker (Switch)
# command = label()
# command.register("create", creat)
# command.register("add", add)
# command.register("exclude", exclude)
# command.register("reset", reset)
# command.register("rename", rename)
# command.register("delete", delete)

# command.execute('create', 'test')
# print(command.history)
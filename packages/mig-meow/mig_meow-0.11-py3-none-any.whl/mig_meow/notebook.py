
import threading

from .workflow_widget import WorkflowWidget
from .monitor_widget import MonitorWidget, update_monitor


def create_workflow_widget(**kwargs):
    """
    Creates and displays a widget for workflow definitions. Passes any given
    keyword arguments to the WorkflowWidget constructor.

    :return: (function call to 'WorkflowWidget.display_widget)
    """

    widget = WorkflowWidget(**kwargs)

    return widget.display_widget()


def create_monitor_widget(**kwargs):
    """
    Creates and displays a widget for monitoring Vgrid job queues. Passes
    any given keyword arguments to the MonitorWidget constructor.

    :return: (function call to 'MonitorWidget.display_widget)
    """

    widget = MonitorWidget(**kwargs)

    monitor_thread = threading.Thread(target=update_monitor, args=(widget,))
    monitor_thread.start()
    return widget.display_widget()

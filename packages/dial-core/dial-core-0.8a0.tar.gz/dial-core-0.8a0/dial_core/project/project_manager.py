# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle
from copy import deepcopy
from typing import TYPE_CHECKING

from dial_core.utils import Timer, log

if TYPE_CHECKING:
    from .project import Project

LOGGER = log.get_logger(__name__)


class ProjectManager:
    """
    The ProjectManager class provides an interface that acts as a container for Project
    objects, and also has the necessary tools to create and open projects from files in
    the system.

    Attributes:
        active: Currently active project.
    """

    def __init__(self, default_project: "Project"):
        self.__default_project = default_project

        self.__projects = [deepcopy(self.__default_project)]

        self.__active = self.__projects[0]

    @property
    def active(self) -> "Project":
        """Returns the currently active project.

        The active project can be accessed directly by using this property.

        See `set_active_project` to learn how to change the active project.
        """
        return self.__active

    def projects_count(self) -> int:
        """Returns the number of created projects."""
        return len(self.__projects)

    def set_active_project(self, index: int) -> "Project":
        """Selects a project from the created ones and makes it the active project.

        Returns:
            The new active project.

        Raises:
            IndexError: If there isn't a project with index `index`.
        """
        self.__active = self.__projects[index]

        LOGGER.info(
            "Active project changed: %s(%s)", index, self.__active,
        )

        return self.__active

    def new_project(self) -> "Project":
        """Adds a new default project to the project manager.

        A copy of a default project (The one defined on the variable
        `self.__default_project` will be added)

        Returns:
            The recently added active project
        """
        new_project = deepcopy(self.__default_project)

        return self.add_project(new_project)

    def add_project(self, project: "Project") -> "Project":
        """Adds a project to the project manager and makes it the new active project.

        Returns:
            The recently added active project.
        """
        self.__projects.append(project)

        return self.set_active_project(self.__projects.index(project))

    def open_project(self, file_path: str) -> "Project":
        """Opens a new project from a `.dial` file.

        Then, the project manager will automatically change its active project to the
        new opened one.

        Returns:
            The opened project (Which is the same as `project_manager.active`)

        Raises:
            FileNotFoundError: If the `file_path` is invalid.
        """
        LOGGER.info("Opening a new project... %s", file_path)

        with open(file_path, "rb") as project_file:
            LOGGER.info("Loading project...")
            with Timer() as timer:
                opened_project = pickle.load(project_file)

                self.add_project(opened_project)

            LOGGER.info("Project loaded in %s ms", timer.elapsed())

            opened_project.file_path = file_path
            LOGGER.info("New project file path is %s", file_path)

        return opened_project

    def save_project(self):
        """Saves the project on its defined file path.

        The project MUST have a file path. Otherwise, it will throw a ValueError
        exception.

        For saving a project specifying a new file path, see `save_project_as`.

        Raises:
            ValueError: If the project doesn't have a `file_path` defined.
        """
        if not self.__active.file_path:
            raise ValueError("Project doesn't has a file_path set!")

        with open(self.active.file_path, "wb") as project_file:
            LOGGER.info("Saving project: %s", self.__active.file_path)

            with Timer() as timer:
                pickle.dump(self.__active, project_file)

            LOGGER.info("Project saved in %s ms", timer.elapsed())

    def save_project_as(self, file_path: str):
        """Save the project on a new file path.

        Once a project has been saved with `save_project_as`, it can also be saved with
        `save_project`, which will use the project's file path automatically.

        Important:
            The new `file_path` will be set as the project file path, replacing any
            previous paths.
        """
        self.active.file_path = file_path
        LOGGER.info("New file path for the project: %s", file_path)

        self.save_project()

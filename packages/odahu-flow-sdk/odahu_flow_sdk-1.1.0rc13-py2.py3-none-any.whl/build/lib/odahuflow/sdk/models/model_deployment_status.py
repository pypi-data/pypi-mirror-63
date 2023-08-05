# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from odahuflow.sdk.models.base_model_ import Model
from odahuflow.sdk.models import util


class ModelDeploymentStatus(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, available_replicas: int=None, created_at: str=None, deployment: str=None, last_revision_name: str=None, last_updated_time: str=None, replicas: int=None, service: str=None, service_url: str=None, state: str=None, updated_at: str=None):  # noqa: E501
        """ModelDeploymentStatus - a model defined in Swagger

        :param available_replicas: The available_replicas of this ModelDeploymentStatus.  # noqa: E501
        :type available_replicas: int
        :param created_at: The created_at of this ModelDeploymentStatus.  # noqa: E501
        :type created_at: str
        :param deployment: The deployment of this ModelDeploymentStatus.  # noqa: E501
        :type deployment: str
        :param last_revision_name: The last_revision_name of this ModelDeploymentStatus.  # noqa: E501
        :type last_revision_name: str
        :param last_updated_time: The last_updated_time of this ModelDeploymentStatus.  # noqa: E501
        :type last_updated_time: str
        :param replicas: The replicas of this ModelDeploymentStatus.  # noqa: E501
        :type replicas: int
        :param service: The service of this ModelDeploymentStatus.  # noqa: E501
        :type service: str
        :param service_url: The service_url of this ModelDeploymentStatus.  # noqa: E501
        :type service_url: str
        :param state: The state of this ModelDeploymentStatus.  # noqa: E501
        :type state: str
        :param updated_at: The updated_at of this ModelDeploymentStatus.  # noqa: E501
        :type updated_at: str
        """
        self.swagger_types = {
            'available_replicas': int,
            'created_at': str,
            'deployment': str,
            'last_revision_name': str,
            'last_updated_time': str,
            'replicas': int,
            'service': str,
            'service_url': str,
            'state': str,
            'updated_at': str
        }

        self.attribute_map = {
            'available_replicas': 'availableReplicas',
            'created_at': 'createdAt',
            'deployment': 'deployment',
            'last_revision_name': 'lastRevisionName',
            'last_updated_time': 'lastUpdatedTime',
            'replicas': 'replicas',
            'service': 'service',
            'service_url': 'serviceURL',
            'state': 'state',
            'updated_at': 'updatedAt'
        }

        self._available_replicas = available_replicas
        self._created_at = created_at
        self._deployment = deployment
        self._last_revision_name = last_revision_name
        self._last_updated_time = last_updated_time
        self._replicas = replicas
        self._service = service
        self._service_url = service_url
        self._state = state
        self._updated_at = updated_at

    @classmethod
    def from_dict(cls, dikt) -> 'ModelDeploymentStatus':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ModelDeploymentStatus of this ModelDeploymentStatus.  # noqa: E501
        :rtype: ModelDeploymentStatus
        """
        return util.deserialize_model(dikt, cls)

    @property
    def available_replicas(self) -> int:
        """Gets the available_replicas of this ModelDeploymentStatus.

        Number of available pods  # noqa: E501

        :return: The available_replicas of this ModelDeploymentStatus.
        :rtype: int
        """
        return self._available_replicas

    @available_replicas.setter
    def available_replicas(self, available_replicas: int):
        """Sets the available_replicas of this ModelDeploymentStatus.

        Number of available pods  # noqa: E501

        :param available_replicas: The available_replicas of this ModelDeploymentStatus.
        :type available_replicas: int
        """

        self._available_replicas = available_replicas

    @property
    def created_at(self) -> str:
        """Gets the created_at of this ModelDeploymentStatus.


        :return: The created_at of this ModelDeploymentStatus.
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at: str):
        """Sets the created_at of this ModelDeploymentStatus.


        :param created_at: The created_at of this ModelDeploymentStatus.
        :type created_at: str
        """

        self._created_at = created_at

    @property
    def deployment(self) -> str:
        """Gets the deployment of this ModelDeploymentStatus.

        The model k8s deployment name  # noqa: E501

        :return: The deployment of this ModelDeploymentStatus.
        :rtype: str
        """
        return self._deployment

    @deployment.setter
    def deployment(self, deployment: str):
        """Sets the deployment of this ModelDeploymentStatus.

        The model k8s deployment name  # noqa: E501

        :param deployment: The deployment of this ModelDeploymentStatus.
        :type deployment: str
        """

        self._deployment = deployment

    @property
    def last_revision_name(self) -> str:
        """Gets the last_revision_name of this ModelDeploymentStatus.

        Last applied ready knative revision  # noqa: E501

        :return: The last_revision_name of this ModelDeploymentStatus.
        :rtype: str
        """
        return self._last_revision_name

    @last_revision_name.setter
    def last_revision_name(self, last_revision_name: str):
        """Sets the last_revision_name of this ModelDeploymentStatus.

        Last applied ready knative revision  # noqa: E501

        :param last_revision_name: The last_revision_name of this ModelDeploymentStatus.
        :type last_revision_name: str
        """

        self._last_revision_name = last_revision_name

    @property
    def last_updated_time(self) -> str:
        """Gets the last_updated_time of this ModelDeploymentStatus.

        Time when credentials was updated  # noqa: E501

        :return: The last_updated_time of this ModelDeploymentStatus.
        :rtype: str
        """
        return self._last_updated_time

    @last_updated_time.setter
    def last_updated_time(self, last_updated_time: str):
        """Sets the last_updated_time of this ModelDeploymentStatus.

        Time when credentials was updated  # noqa: E501

        :param last_updated_time: The last_updated_time of this ModelDeploymentStatus.
        :type last_updated_time: str
        """

        self._last_updated_time = last_updated_time

    @property
    def replicas(self) -> int:
        """Gets the replicas of this ModelDeploymentStatus.

        Expected number of pods under current load  # noqa: E501

        :return: The replicas of this ModelDeploymentStatus.
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas: int):
        """Sets the replicas of this ModelDeploymentStatus.

        Expected number of pods under current load  # noqa: E501

        :param replicas: The replicas of this ModelDeploymentStatus.
        :type replicas: int
        """

        self._replicas = replicas

    @property
    def service(self) -> str:
        """Gets the service of this ModelDeploymentStatus.

        The model k8s service name  # noqa: E501

        :return: The service of this ModelDeploymentStatus.
        :rtype: str
        """
        return self._service

    @service.setter
    def service(self, service: str):
        """Sets the service of this ModelDeploymentStatus.

        The model k8s service name  # noqa: E501

        :param service: The service of this ModelDeploymentStatus.
        :type service: str
        """

        self._service = service

    @property
    def service_url(self) -> str:
        """Gets the service_url of this ModelDeploymentStatus.

        The model k8s service name  # noqa: E501

        :return: The service_url of this ModelDeploymentStatus.
        :rtype: str
        """
        return self._service_url

    @service_url.setter
    def service_url(self, service_url: str):
        """Sets the service_url of this ModelDeploymentStatus.

        The model k8s service name  # noqa: E501

        :param service_url: The service_url of this ModelDeploymentStatus.
        :type service_url: str
        """

        self._service_url = service_url

    @property
    def state(self) -> str:
        """Gets the state of this ModelDeploymentStatus.

        The state of a model    \"Processing\" - A model was not deployed. Because some parameters of the                  custom resource are wrong. For example, there is not a model                  image in a Docker registry.   \"Ready\" - A model was deployed successfully.  # noqa: E501

        :return: The state of this ModelDeploymentStatus.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state: str):
        """Sets the state of this ModelDeploymentStatus.

        The state of a model    \"Processing\" - A model was not deployed. Because some parameters of the                  custom resource are wrong. For example, there is not a model                  image in a Docker registry.   \"Ready\" - A model was deployed successfully.  # noqa: E501

        :param state: The state of this ModelDeploymentStatus.
        :type state: str
        """

        self._state = state

    @property
    def updated_at(self) -> str:
        """Gets the updated_at of this ModelDeploymentStatus.


        :return: The updated_at of this ModelDeploymentStatus.
        :rtype: str
        """
        return self._updated_at

    @updated_at.setter
    def updated_at(self, updated_at: str):
        """Sets the updated_at of this ModelDeploymentStatus.


        :param updated_at: The updated_at of this ModelDeploymentStatus.
        :type updated_at: str
        """

        self._updated_at = updated_at

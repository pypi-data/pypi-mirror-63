# -*- coding: utf-8 -*-
#
# Copyright 2020 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Renku service dataset jobs tests."""
import json

import pytest
from flaky import flaky
from git import Repo
from tests.service.views.test_dataset_views import assert_rpc_response

from renku.core.errors import DatasetExistsError, ParameterError
from renku.service.jobs.datasets import dataset_import
from renku.service.utils import make_project_path


@pytest.mark.parametrize(
    'doi', [
        '10.5281/zenodo.3239980',
        '10.5281/zenodo.3188334',
        '10.7910/DVN/TJCLKP',
    ]
)
@pytest.mark.integration
@pytest.mark.service
@flaky(max_runs=30, min_passes=1)
def test_dataset_import_job(doi, svc_client_with_repo):
    """Test dataset import."""
    svc_client, headers, project_id, url_components = svc_client_with_repo
    user = {'user_id': headers['Renku-User-Id']}
    payload = {
        'project_id': project_id,
        'dataset_uri': doi,
    }
    response = svc_client.post(
        '/datasets.import',
        data=json.dumps(payload),
        headers=headers,
    )

    assert response
    assert_rpc_response(response)
    assert {'job_id', 'created_at'} == set(response.json['result'].keys())

    dest = make_project_path(
        user, {
            'owner': url_components.owner,
            'name': url_components.name
        }
    )

    old_commit = Repo(dest).head.commit

    dataset_import(
        user,
        response.json['result']['job_id'],
        project_id,
        doi,
    )

    new_commit = Repo(dest).head.commit
    assert old_commit.hexsha != new_commit.hexsha
    assert f'service: dataset import {doi}' == new_commit.message


@pytest.mark.parametrize(
    'doi,expected_err',
    [
        # not valid doi
        ('junkjunkjunk', 'Invalid parameter value'),
        # not existing doi
        ('10.5281/zenodo.11111111111111111', 'Invalid parameter value'),
    ]
)
@pytest.mark.integration
@pytest.mark.service
def test_dataset_import_junk_job(doi, expected_err, svc_client_with_repo):
    """Test dataset import."""
    svc_client, headers, project_id, url_components = svc_client_with_repo
    user = {'user_id': headers['Renku-User-Id']}
    payload = {
        'project_id': project_id,
        'dataset_uri': doi,
    }
    response = svc_client.post(
        '/datasets.import',
        data=json.dumps(payload),
        headers=headers,
    )

    assert response
    assert_rpc_response(response)
    assert {'job_id', 'created_at'} == set(response.json['result'].keys())

    dest = make_project_path(
        user, {
            'owner': url_components.owner,
            'name': url_components.name
        }
    )

    old_commit = Repo(dest).head.commit
    job_id = response.json['result']['job_id']

    with pytest.raises(ParameterError):
        dataset_import(
            user,
            job_id,
            project_id,
            doi,
        )

    new_commit = Repo(dest).head.commit
    assert old_commit.hexsha == new_commit.hexsha

    response = svc_client.get(
        f'/jobs/{job_id}',
        data=json.dumps(payload),
        headers=headers,
    )

    assert_rpc_response(response)
    extras = response.json['result']['extras']

    assert 'error' in extras
    assert expected_err in extras['error']


@pytest.mark.parametrize('doi', [
    '10.5281/zenodo.3634052',
])
@pytest.mark.integration
@pytest.mark.service
def test_dataset_import_twice_job(doi, svc_client_with_repo):
    """Test dataset import."""
    svc_client, headers, project_id, url_components = svc_client_with_repo
    user = {'user_id': headers['Renku-User-Id']}
    payload = {
        'project_id': project_id,
        'dataset_uri': doi,
    }
    response = svc_client.post(
        '/datasets.import',
        data=json.dumps(payload),
        headers=headers,
    )

    assert response
    assert_rpc_response(response)
    assert {'job_id', 'created_at'} == set(response.json['result'].keys())

    dest = make_project_path(
        user, {
            'owner': url_components.owner,
            'name': url_components.name
        }
    )

    old_commit = Repo(dest).head.commit
    job_id = response.json['result']['job_id']

    dataset_import(
        user,
        job_id,
        project_id,
        doi,
    )

    new_commit = Repo(dest).head.commit
    assert old_commit.hexsha != new_commit.hexsha

    with pytest.raises(DatasetExistsError):
        dataset_import(
            user,
            job_id,
            project_id,
            doi,
        )

    new_commit2 = Repo(dest).head.commit
    assert new_commit.hexsha == new_commit2.hexsha

    response = svc_client.get(
        f'/jobs/{job_id}',
        data=json.dumps(payload),
        headers=headers,
    )

    assert_rpc_response(response)
    extras = response.json['result']['extras']

    assert 'error' in extras
    assert 'Dataset exists' in extras['error']

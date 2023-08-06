#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import logging

from eth_utils import add_0x_prefix
from ocean_keeper.keeper import Keeper
from ocean_keeper.utils import process_fulfill_condition
from ocean_utils.did import did_to_id

logger = logging.getLogger(__name__)


def fulfill_compute_execution_condition(event, agreement_id, did, service_agreement,
                                   consumer_address, publisher_account, compute_execution_condition_id):
    """
    Fulfill the compute execution condition.

    :param event: AttributeDict with the event data.
    :param agreement_id: id of the agreement, hex str
    :param did: DID, str
    :param service_agreement: ServiceAgreement instance
    :param consumer_address: ethereum account address of consumer, hex str
    :param publisher_account: Account instance of the publisher
    :param compute_execution_condition_id: hex str the id of the compute execution condition for this
        `agreement_id`
    """
    if not event:
        logger.debug(f'`fulfill_exec_compute_condition` got empty event: '
                     f'event listener timed out.')
        return

    keeper = Keeper.get_instance()
    if keeper.condition_manager.get_condition_state(compute_execution_condition_id) > 1:
        logger.debug(
            f'compute execution condition already fulfilled/aborted: '
            f'agreementId={agreement_id}, compute execution conditionId={compute_execution_condition_id}'
        )
        return

    logger.debug(f"grant access (agreement {agreement_id}) after event {event}.")
    name_to_parameter = {param.name: param for param in
                         service_agreement.condition_by_name['computeExecution'].parameters}
    document_id = add_0x_prefix(name_to_parameter['_documentId'].value)
    asset_id = add_0x_prefix(did_to_id(did))
    assert document_id == asset_id, f'document_id {document_id} <=> asset_id {asset_id} mismatch.'

    args = (
        agreement_id,
        document_id,
        consumer_address,
        publisher_account
    )
    process_fulfill_condition(args, keeper.compute_execution_condition, compute_execution_condition_id,
                              logger, keeper, 10)


fulfillComputeExecutionCondition = fulfill_compute_execution_condition

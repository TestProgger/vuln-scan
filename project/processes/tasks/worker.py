from config.celery import app as celery_app
from project.processes.tasks.consts import TaskKwarg
from project.scenarios.models import ScenarioBlock
from project.workers.manager import worker_manager
from project.workers.os.exploit.manager import exploit_manager
from project.processes.tasks.utils import depth_extractor
from project.processes.models import ProcessTrigger, ProcessTriggerMessage
from project.workers.os.exploit.vsftpd_cve_2011_2523 import VsftpdExploit
import json


@celery_app.task()
def run_exploit(**kwargs):
    process_id = kwargs.get(TaskKwarg.PROCESS_ID.value)
    exploit_body = kwargs.get(TaskKwarg.EXPLOIT_BODY.value)
    exploit_name = kwargs.get(TaskKwarg.EXPLOIT_NAME.value)
    scenario_block_id = kwargs.get(TaskKwarg.SCENARIO_BLOCK_ID.value)

    trigger = ProcessTrigger.objects.create(
        process_id=process_id,
        scenario_block_id=scenario_block_id
    )

    result = exploit_manager.handle(exploit_name, **exploit_body)

    ProcessTriggerMessage.objects.create(
        trigger=trigger,
        value=json.dumps(result)
    )

    trigger.is_completed = True
    trigger.save()


@celery_app.task()
def worker(**kwargs):
    process_id = kwargs.get(TaskKwarg.PROCESS_ID.value)
    worker_body = kwargs.get(TaskKwarg.WORKER_BODY.value)
    instruction = kwargs.get(TaskKwarg.INSTRUCTION.value)
    parent_instruction = kwargs.get(TaskKwarg.PARENT_INSTRUCTION.value)
    scenario_block_id = kwargs.get(TaskKwarg.SCENARIO_BLOCK_ID.value)

    trigger = ProcessTrigger.objects.create(
        process_id=process_id,
        scenario_block_id=scenario_block_id
    )

    result, is_success = worker_manager.handle(parent_instruction, instruction, **worker_body)

    ProcessTriggerMessage.objects.create(
        trigger=trigger,
        value=json.dumps(result)
    )

    try:
        if worker_body.get("exploit"):
            exploits, obj = depth_extractor(result, "vulns")
            for exploit in exploits:
                run_exploit.apply_async(
                    kwargs={
                        TaskKwarg.PROCESS_ID.value: process_id,
                        TaskKwarg.EXPLOIT_BODY.value: obj,
                        TaskKwarg.EXPLOIT_NAME.value: exploit,
                        TaskKwarg.SCENARIO_BLOCK_ID.value: scenario_block_id
                    }
                )
    except:
        pass

    trigger.is_completed = True
    trigger.save()


@celery_app.task()
def run_workers(**kwargs):
    # user_id = kwargs.get(TaskKwarg.USER_ID.value)
    scenario_id = kwargs.get(TaskKwarg.SCENARIO_ID.value)
    process_id = kwargs.get(TaskKwarg.PROCESS_ID.value)

    scenario_blocks = ScenarioBlock.objects.filter(
        scenario_id=scenario_id,
        parent_id__isnull=False
    )

    for scenario_block in scenario_blocks:
        worker.apply_async(
            kwargs={
                TaskKwarg.SCENARIO_BLOCK_ID.value: scenario_block.id,
                TaskKwarg.PROCESS_ID.value: process_id,
                TaskKwarg.INSTRUCTION.value: scenario_block.instruction,
                TaskKwarg.PARENT_INSTRUCTION.value: scenario_block.parent_instruction,
                TaskKwarg.WORKER_BODY.value: scenario_block.value
            }
        )

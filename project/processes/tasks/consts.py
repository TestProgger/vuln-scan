from enum import Enum


class TaskKwarg(Enum):
    USER_ID = "user_id"
    SCENARIO_ID = "scenario_id"
    PROCESS_ID = "process_id"
    WORKER_BODY = "worker_body"
    EXPLOIT_BODY = "exploit_body"
    EXPLOIT_NAME = "exploit_name"
    INSTRUCTION = "instruction"
    PARENT_INSTRUCTION = "parent_instruction"
    SCENARIO_BLOCK_ID = "scenario_block_id"
    PROCESS_TRIGGER_MESSAGE_ID = "process_trigger_message_id"


class CountdownTask(Enum):
    CHECK_PROCESS_COMPLETED = 5
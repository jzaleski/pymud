from pymud.network import ClientConnectionManager


class BaseCommandHandler(object):
    def __init__(
        self,
        command,
        audible_or_visual_range=0,
        cannot_execute_command_message="You can't do that right now",
        resulting_state=None
    ):
        assert audible_or_visual_range >= 0
        self._command = command
        self._audible_or_visual_range = audible_or_visual_range
        self._cannot_execute_command_message = cannot_execute_command_message
        self._resulting_state = resulting_state

    def handle(
        self,
        source,
        args
    ):
        source_character = source.character
        if not self._can_execute_command(source):
            source.send(self._cannot_execute_command_message)
            return
        resulting_state = self._resulting_state
        if resulting_state and source_character.state == resulting_state:
            source.send('You are already %s' % resulting_state)
            return
        result = self._execute_range_function(
            0,
            source,
            args
        )
        if result is not None:
            if resulting_state is not None:
                source_character.state = resulting_state
            source.send(result)
        handled_client_connections = [source]
        for distance in range(1, self._audible_or_visual_range + 1):
            matching_client_connections = \
                ClientConnectionManager.instance.get_all_except(handled_client_connections,
                    exclude_waiting_for_name=True)
            result = self._execute_range_function(
                distance,
                source,
                args
            )
            for matching_client_connection in matching_client_connections:
                if result is not None:
                    matching_client_connection.send(result)
                handled_client_connections.append(matching_client_connection)

    def _can_execute_command(self, source):
        return True

    def _execute_range_function(
        self,
        distance,
        source,
        args
    ):
        range_function = getattr(
            self,
            'range_%s' % distance,
            None
        )
        if not range_function:
            return None
        return range_function(source, args)

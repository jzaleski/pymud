from pymud.network import ClientConnectionManager

class BaseCommandHandler(object):

    def __init__(
        self,
        command,
        audible_or_visual_range=0,
        cannot_execute_command_message="You can't do that right now"
    ):
        assert audible_or_visual_range >= 0
        self.__command = command
        self.__audible_or_visual_range = audible_or_visual_range
        self.__cannot_execute_command_message = cannot_execute_command_message

    def handle(self, source, args):
        if not self._can_execute_command(source):
            source.send(self.__cannot_execute_command_message)
            return
        result = self.__execute_range_function(
            0,
            source,
            args
        )
        if result != None:
            source.send(result)
        handled_client_connections = [source]
        for distance in range(1, self.__audible_or_visual_range + 1):
            matching_client_connections = \
                ClientConnectionManager.instance.get_all_except(
                    handled_client_connections,
                    exclude_waiting_for_name=True
                )
            result = self.__execute_range_function(
                distance,
                source,
                args
            )
            for matching_client_connection in matching_client_connections:
                if result != None:
                    matching_client_connection.send(
                        result,
                        num_leading_new_lines=1
                    )
                handled_client_connections.append(matching_client_connection)

    def _can_execute_command(self, source):
        return True

    def __execute_range_function(self, distance, source, args):
        range_function = getattr(
            self,
            'range_%s' % distance,
            None
        )
        if not range_function:
            return None
        return range_function(
            source,
            args
        )

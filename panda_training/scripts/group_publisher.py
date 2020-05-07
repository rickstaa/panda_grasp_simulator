"""Class used to group a number of publishers together.
"""

# ROS python imports
import rospy


#################################################
# Group Publisher class #########################
#################################################
class GroupPublisher(list):
    """Used for bundling ROS publishers together and publishing
    to these publishers at the same time.

    Methods
    -------
    publish(messages):
        Publish messages to all publishers.
    """

    def __init__(self, iterable=[]):
        """
        Parameters
        ----------
        iterable : iterable, optional
            New list initialized from iterable items, by default [].

        Raises
        ------
        ValueError
            If list does not only contain ROS publishers.
        """

        # Validate if list contains publisher objects
        if type(iterable) is list:
            for publisher in iterable:
                if type(publisher) is not rospy.Publisher:
                    raise ValueError(
                        "Please supply a list containing only ros publishers."
                    )
        else:
            if type(iterable) is not rospy.Publisher:
                raise ValueError("Please supply a list containing only ros publishers.")

        # Call superclass initation method
        super(GroupPublisher, self).__init__(iterable)

    def publish(self, messages):
        """Publishes a list of messages to the publishers contained on the
        GroupPublisher object. The index of the message corresponds to the
        publisher the message will be published to.

        Parameters
        ----------
        messages : list
            List containing the messages to be published.

        Raises
        ------
        ValueError
        """

        # Validate input messages
        if self.__len__() == 0:
            raise ValueError(
                "Message could not be published since GroupPublisher "
                "contains no publishers."
            )
        elif self.__len__() > 1 and type(messages) is not list:
            raise ValueError(
                "Only one message was given while the GroupPublisher object "
                "contains %s publishers. Please input a list containing %s ROS "
                "messages." % (self.__len__(), self.__len__())
            )
        elif self.__len__() > 1 and type(messages) is list:
            if self.__len__() != len(messages):
                raise ValueError(
                    "%s messages were given while the GroupPublisher object "
                    "contains %s publishers. Please input a list containing %s ROS "
                    "messages." % (len(messages), self.__len__(), self.__len__())
                )

        # Publish messages to the publishers
        if type(messages) is not list:
            self[0].publish(messages)
        else:
            for ii in range(len(messages)):
                self[ii].publish(messages[ii])

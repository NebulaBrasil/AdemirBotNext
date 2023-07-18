from uuid import UUID
from models.play_mode import PlayMode
from models.playback_state import PlaybackState

class AdemirCfg:
    def __init__(self: str, 
                 AdemirConfigId: UUID = None, 
                 GuildId: int = None, 
                 GlobalVolume: int = None,
                 PlaybackState: PlaybackState = None,
                 PlayMode: PlayMode = None,
                 VoiceChannel: int = None,
                 Position: float = None,
                 CurrentTrack: int = None,
                 AdemirRoleId: int = None,
                 AdemirConversationRPM: int = None,
                 Premium: bool = False):
        self.AdemirConfigId = AdemirConfigId
        self.GuildId = GuildId
        self.GlobalVolume = GlobalVolume
        self.PlaybackState = PlaybackState
        self.PlayMode = PlayMode
        self.VoiceChannel = VoiceChannel
        self.Position = Position
        self.CurrentTrack = CurrentTrack
        self.AdemirRoleId = AdemirRoleId
        self.AdemirConversationRPM = AdemirConversationRPM
        self.Premium = Premium
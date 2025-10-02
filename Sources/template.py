from	typing			import Optional
from	dataclasses		import dataclass

@dataclass
class User:
	login:		str
	name:		Optional[str] = None
	location:	Optional[str] = None
	gender:		Optional[int] = 0
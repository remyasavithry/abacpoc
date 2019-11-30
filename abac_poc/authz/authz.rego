package system

main = allow

default allow = false

allow {
	input.resource.type == "opportunity"
    has_role("advisor", user)
}

allow {
	input.resource.type == "opportunity"
    has_role("manager", user)
    input.user.id == input.resource.author
}

allow {
	input.resource.type == "opportunity"
    has_role("manager", user)
    input.user.id == input.resource.managed_by
}

allow {
	input.resource.type == "opportunity"
	has_role("associate", user)
	input.user.company == input.resource.company
}

has_role(name, user) {
	user.roles[_] = name
}

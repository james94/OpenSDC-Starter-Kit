variable "TAG" {
 default = "latest"   
}

variable "REGISTRY" {
    default = "open_sdc"
}

group "default" {
    targets = ["sdc_apt", "sdc_backend"]
}

##
# OpenSDC Backend
##
target "sdc_apt" {
    context = "../src/build_image/sdc_backend/sdc_apt"
    tags = ["${REGISTRY}/sdc_apt:${TAG}"]
    platforms = ["linux/amd64"]
}

target "sdc_backend" {
    context = "../src/build_image/sdc_backend/sdc_entries"
    contexts = {
        sdc_apt = "target:sdc_apt"
    }
    tags = ["${REGISTRY}/sdc_entries:${TAG}", "${REGISTRY}/sdc_backend:${TAG}"]
}

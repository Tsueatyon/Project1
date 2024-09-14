<template>
    <div style="margin-top: 25px">
      <Row style="text-align:center;display: inline">
        <h1>student grade management system</h1>
      </Row>
    </div>
    <div style="margin-top: 10px">
      <Row>
        <Col span="8" offset="8">
            <Row style="margin-top: 10px">
              <Col span="4"><h3>UserName</h3></Col>
              <Col span="20"><Input v-model="name"/></Col>
            </Row>
            <Row style="margin-top: 10px">
              <Col span="4">  <h3>Password</h3></Col>
              <Col span="20"><Input type="password" v-model="password"/></Col>
            </Row>
            <Row style="margin-top: 10px">
              <Col offset="4" span="20">
                <Button type="success" long @click='login'>SUBMIT</Button>
              </Col>
            </Row>
        </Col>
      </Row>
    </div>
</template>

<script>


export default {

  data() {
    return {
      name: '',
      password: '',
    };
  },
  methods: {
    login() {
      if (this.name == '') {
        this.$Message.info('Please enter username');
        return
      }
      if (this.password == '') {
        this.$Message.info('Please enter password');
        return
      }
      const pack = {name: this.name, password: this.password}
      console.log(pack)
      this.$axios({
        withCredentials: true,
        method: "post",
        url: "http://localhost:9000/login",
        data: JSON.stringify(pack),
        headers: {
          'Content-Type': 'application/json',
        }
      }).then((res) => {
        console.log(res)
        if (res.status!=200) {
          this.$Message.error('API error+('+res.status+')')
        }
        if (res.data.code===999){
          this.$Message.error(res.data.message)
          this.$router.push('./login')
          return
        }
        if (res.data.code==0){
          this.$Message.success(res.data.message)
          this.$router.push('/students')
          return;
        }else{
          this.$Message.error(res.data.message)
          return;
        }
      }).catch((err)=>{
        this.$Message.error('internet error('+err+')')
      })
    },
  }
}

</script>
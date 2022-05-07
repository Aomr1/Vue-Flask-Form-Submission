<template>
  <div class="home_box">
    <el-row :gutter="20" style="margin-left: 0px; margin-right: 0px">
      <el-col :span="2" style="margin-top: 15px">
        <el-button type="primary" plain size="small" @click="handleAdd"
          >添加活动</el-button
        >
      </el-col>
      <el-col :span="22" style="margin-top: 15px" class="form-search">
        <div style="float: right">
          <el-input
            v-model="keywords"
            placeholder="请输入邮箱名进行搜索"
            style="width: 200px; color: #606266"
            plain
            size="small"
            @keyup.enter.native="search"
          >
          </el-input>
          <el-button-group>
            <el-button type="primary" @click="search" plain size="small"
              >搜索</el-button
            >
            <el-button type="primary" @click="clearkeyword" plain size="small"
              >清空</el-button
            >
          </el-button-group>
        </div>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-left: 0px; margin-right: 0px">
      <el-col :span="24" style="margin-top: 15px">
        <el-carousel
          :interval="10000"
          height="600px"
          indicator-position="outside"
        >
          <el-carousel-item
            v-for="item in tableData"
            :index="item.id"
            :key="item.id"
          >
            <el-card shadow="hover" class="form_card">
              <el-descriptions
                style="margin-top: 20px"
                title="活动信息"
                size="medium"
                :column="4"
                direction="vertical"
                border
                v-loading="loading"
                element-loading-text="拼命加载中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
              >
                <template slot="extra">
                  <el-button
                    type="primary"
                    size="small"
                    @click="handleDelete(item.id)"
                    >删除</el-button
                  >
                </template>
                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-collection-tag"></i>
                    活动邮箱
                  </template>
                  {{ item.email }}
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-star-off"></i>
                    活动名称
                  </template>
                  {{ item.name }}
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-location-outline"></i>
                    活动区域
                  </template>
                  {{ item.region }}
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-time"></i>
                    活动时间
                  </template>
                  {{ item.date }}
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-tickets"></i>
                    活动认证
                  </template>
                  <template v-if="item.delivery === 'True'">有认证</template>
                  <template v-if="item.delivery === 'False'">无认证</template>
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-document"></i>
                    活动性质
                  </template>
                  <div
                    style="margin-bottom: 2px"
                    v-for="(item_type, index) in item.type"
                    :key="index"
                  >
                    {{ item_type }}
                  </div>
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-umbrella"></i>
                    活动资源
                  </template>
                  {{ item.resource }}
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-news"></i>
                    活动形式
                  </template>
                  {{ item.desc }}
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-picture"></i>
                    活动图片
                  </template>
                  <div
                    class="block-content"
                    v-for="(item_imagename, index) in item.imageName"
                    :key="index"
                    :ref="index"
                  >
                    <el-avatar
                      class="l-content"
                      :title="item_imagename"
                      shape="square"
                      :size="120"
                      :src="localhost + item_imagename"
                    ></el-avatar>
                    <el-link
                      class="r-content"
                      :href="localhost + item_imagename"
                      target="_blank"
                      :underline="false"
                      >查看<i class="el-icon-view el-icon--right"></i>
                    </el-link>
                  </div>
                </el-descriptions-item>

                <el-descriptions-item>
                  <template slot="label">
                    <i class="el-icon-folder-opened"></i>
                    活动文件
                  </template>
                  <div
                    class="block-content"
                    v-for="(item_filename, index) in item.fileName"
                    :key="index"
                    :ref="index"
                    style="margin-bottom: 5px"
                  >
                    <el-tag class="l-content"
                      ><i class="el-icon-folder"></i>{{ item_filename }}</el-tag
                    >
                    <el-link
                      class="r-content"
                      :href="localhost + item_filename"
                      target="_blank"
                      :underline="false"
                      >下载<i class="el-icon-download el-icon--right"></i>
                    </el-link>
                  </div>
                </el-descriptions-item>
              </el-descriptions>
            </el-card>
          </el-carousel-item>
        </el-carousel>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      keywords: "",
      tableData: [],
      list:[],
      loading: true,
      delete_id: "",
      localhost: "http://localhost:5000/static/",
    };
  },
  methods: {
    get_tableData() {
      this.$axios
        .get("http://127.0.0.1:5000/User/SelectForms")
        .then((response) => {
          this.tableData = response.data;
          this.list = response.data
          this.loading = false;
        });
    },
    handleAdd() {
      this.$router.push({
        name: "Form",
      });
    },
    handleDelete(index, row) {
      this.delete_id = row.id;
      console.log(index, row.id);
    },
    fail() {
      this.$message({
        message: "已取消修改！",
        center: true,
        type: "info",
      });
    },
    success() {
      this.$message({
        message: "修改成功！",
        center: true,
        type: "success",
      });
      setTimeout(function () {
        window.location.reload();
      }, 1700);
    },
    clearkeyword() {
      this.keywords = "";
    },
    handleDelete(id) {
      this.$confirm("此操作将永久删除该表单, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
        this.$axios
          .post("http://127.0.0.1:5000/User/DeleteForm", { delete_id: id })
          .then((response) => {
            if (response.data.code == 200) {
              this.$message({
                type: "success",
                message: "删除成功!",
              });
               setTimeout(function(){window.location.reload()},1700);
            }
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消删除",
            });
          });
      });
    },
    search() {
      this.tableData = this.tableData.filter((item) => {
        return item.email.indexOf(this.keywords) !== -1;
      });
    },
  },
  mounted() {
    this.get_tableData();
  },
  watch: {
    keywords() {
      if (this.keywords == "") {
        this.tableData = this.list;
      }
    },
  },
};
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
.home_box {
  width: 1500px;
  text-align: center;
  margin: 0 auto;
  line-height: auto;
}
.form-search .el-input__inner {
  background-color: #fff;
  color: #606266;
}
.form_card .el-card__body {
  padding-top: 0;
  padding-left: 60px;
  padding-right: 60px;
  margin-bottom: 10px;
}
.block-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.l-content {
  display: flex;
  align-items: center;
  vertical-align: middle;
}
.r-content {
  display: flex;
  align-items: center;
  vertical-align: middle;
}
</style>
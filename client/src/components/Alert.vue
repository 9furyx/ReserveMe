<template>
  <div>
    <b-alert :variant= 'alertvariant' show>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>
export default {
  props: ['message', 'alertvariant'],
};
</script>

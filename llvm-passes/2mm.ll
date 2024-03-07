; ModuleID = '2mm.c'
source_filename = "2mm.c"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

@.str = private unnamed_addr constant [1 x i8] zeroinitializer, align 1
@stderr = external global ptr, align 8
@.str.1 = private unnamed_addr constant [23 x i8] c"==BEGIN DUMP_ARRAYS==\0A\00", align 1
@.str.2 = private unnamed_addr constant [15 x i8] c"begin dump: %s\00", align 1
@.str.3 = private unnamed_addr constant [2 x i8] c"D\00", align 1
@.str.4 = private unnamed_addr constant [2 x i8] c"\0A\00", align 1
@.str.5 = private unnamed_addr constant [8 x i8] c"%0.2lf \00", align 1
@.str.6 = private unnamed_addr constant [17 x i8] c"\0Aend   dump: %s\0A\00", align 1
@.str.7 = private unnamed_addr constant [23 x i8] c"==END   DUMP_ARRAYS==\0A\00", align 1

; Function Attrs: noinline nounwind optnone uwtable
define dso_local i32 @main(i32 noundef %0, ptr noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  %5 = alloca ptr, align 8
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  %9 = alloca i32, align 4
  %10 = alloca double, align 8
  %11 = alloca double, align 8
  %12 = alloca ptr, align 8
  %13 = alloca ptr, align 8
  %14 = alloca ptr, align 8
  %15 = alloca ptr, align 8
  %16 = alloca ptr, align 8
  store i32 0, ptr %3, align 4
  store i32 %0, ptr %4, align 4
  store ptr %1, ptr %5, align 8
  store i32 800, ptr %6, align 4
  store i32 900, ptr %7, align 4
  store i32 1100, ptr %8, align 4
  store i32 1200, ptr %9, align 4
  %17 = call ptr @polybench_alloc_data(i64 noundef 720000, i32 noundef 8)
  store ptr %17, ptr %12, align 8
  %18 = call ptr @polybench_alloc_data(i64 noundef 880000, i32 noundef 8)
  store ptr %18, ptr %13, align 8
  %19 = call ptr @polybench_alloc_data(i64 noundef 990000, i32 noundef 8)
  store ptr %19, ptr %14, align 8
  %20 = call ptr @polybench_alloc_data(i64 noundef 1080000, i32 noundef 8)
  store ptr %20, ptr %15, align 8
  %21 = call ptr @polybench_alloc_data(i64 noundef 960000, i32 noundef 8)
  store ptr %21, ptr %16, align 8
  %22 = load i32, ptr %6, align 4
  %23 = load i32, ptr %7, align 4
  %24 = load i32, ptr %8, align 4
  %25 = load i32, ptr %9, align 4
  %26 = load ptr, ptr %13, align 8
  %27 = getelementptr inbounds [800 x [1100 x double]], ptr %26, i64 0, i64 0
  %28 = load ptr, ptr %14, align 8
  %29 = getelementptr inbounds [1100 x [900 x double]], ptr %28, i64 0, i64 0
  %30 = load ptr, ptr %15, align 8
  %31 = getelementptr inbounds [900 x [1200 x double]], ptr %30, i64 0, i64 0
  %32 = load ptr, ptr %16, align 8
  %33 = getelementptr inbounds [800 x [1200 x double]], ptr %32, i64 0, i64 0
  call void @init_array(i32 noundef %22, i32 noundef %23, i32 noundef %24, i32 noundef %25, ptr noundef %10, ptr noundef %11, ptr noundef %27, ptr noundef %29, ptr noundef %31, ptr noundef %33)
  %34 = load i32, ptr %6, align 4
  %35 = load i32, ptr %7, align 4
  %36 = load i32, ptr %8, align 4
  %37 = load i32, ptr %9, align 4
  %38 = load double, ptr %10, align 8
  %39 = load double, ptr %11, align 8
  %40 = load ptr, ptr %12, align 8
  %41 = getelementptr inbounds [800 x [900 x double]], ptr %40, i64 0, i64 0
  %42 = load ptr, ptr %13, align 8
  %43 = getelementptr inbounds [800 x [1100 x double]], ptr %42, i64 0, i64 0
  %44 = load ptr, ptr %14, align 8
  %45 = getelementptr inbounds [1100 x [900 x double]], ptr %44, i64 0, i64 0
  %46 = load ptr, ptr %15, align 8
  %47 = getelementptr inbounds [900 x [1200 x double]], ptr %46, i64 0, i64 0
  %48 = load ptr, ptr %16, align 8
  %49 = getelementptr inbounds [800 x [1200 x double]], ptr %48, i64 0, i64 0
  call void @kernel_2mm(i32 noundef %34, i32 noundef %35, i32 noundef %36, i32 noundef %37, double noundef %38, double noundef %39, ptr noundef %41, ptr noundef %43, ptr noundef %45, ptr noundef %47, ptr noundef %49)
  %50 = load i32, ptr %4, align 4
  %51 = icmp sgt i32 %50, 42
  br i1 %51, label %52, label %63

52:                                               ; preds = %2
  %53 = load ptr, ptr %5, align 8
  %54 = getelementptr inbounds ptr, ptr %53, i64 0
  %55 = load ptr, ptr %54, align 8
  %56 = call i32 @strcmp(ptr noundef %55, ptr noundef @.str) #5
  %57 = icmp ne i32 %56, 0
  br i1 %57, label %63, label %58

58:                                               ; preds = %52
  %59 = load i32, ptr %6, align 4
  %60 = load i32, ptr %9, align 4
  %61 = load ptr, ptr %16, align 8
  %62 = getelementptr inbounds [800 x [1200 x double]], ptr %61, i64 0, i64 0
  call void @print_array(i32 noundef %59, i32 noundef %60, ptr noundef %62)
  br label %63

63:                                               ; preds = %58, %52, %2
  %64 = load ptr, ptr %12, align 8
  call void @free(ptr noundef %64) #6
  %65 = load ptr, ptr %13, align 8
  call void @free(ptr noundef %65) #6
  %66 = load ptr, ptr %14, align 8
  call void @free(ptr noundef %66) #6
  %67 = load ptr, ptr %15, align 8
  call void @free(ptr noundef %67) #6
  %68 = load ptr, ptr %16, align 8
  call void @free(ptr noundef %68) #6
  ret i32 0
}

declare ptr @polybench_alloc_data(i64 noundef, i32 noundef) #1

; Function Attrs: noinline nounwind optnone uwtable
define internal void @init_array(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3, ptr noundef %4, ptr noundef %5, ptr noundef %6, ptr noundef %7, ptr noundef %8, ptr noundef %9) #0 {
  %11 = alloca i32, align 4
  %12 = alloca i32, align 4
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca ptr, align 8
  %16 = alloca ptr, align 8
  %17 = alloca ptr, align 8
  %18 = alloca ptr, align 8
  %19 = alloca ptr, align 8
  %20 = alloca ptr, align 8
  %21 = alloca i32, align 4
  %22 = alloca i32, align 4
  store i32 %0, ptr %11, align 4
  store i32 %1, ptr %12, align 4
  store i32 %2, ptr %13, align 4
  store i32 %3, ptr %14, align 4
  store ptr %4, ptr %15, align 8
  store ptr %5, ptr %16, align 8
  store ptr %6, ptr %17, align 8
  store ptr %7, ptr %18, align 8
  store ptr %8, ptr %19, align 8
  store ptr %9, ptr %20, align 8
  %23 = load ptr, ptr %15, align 8
  store double 1.500000e+00, ptr %23, align 8
  %24 = load ptr, ptr %16, align 8
  store double 1.200000e+00, ptr %24, align 8
  store i32 0, ptr %21, align 4
  br label %25

25:                                               ; preds = %56, %10
  %26 = load i32, ptr %21, align 4
  %27 = load i32, ptr %11, align 4
  %28 = icmp slt i32 %26, %27
  br i1 %28, label %29, label %59

29:                                               ; preds = %25
  store i32 0, ptr %22, align 4
  br label %30

30:                                               ; preds = %52, %29
  %31 = load i32, ptr %22, align 4
  %32 = load i32, ptr %13, align 4
  %33 = icmp slt i32 %31, %32
  br i1 %33, label %34, label %55

34:                                               ; preds = %30
  %35 = load i32, ptr %21, align 4
  %36 = load i32, ptr %22, align 4
  %37 = mul nsw i32 %35, %36
  %38 = add nsw i32 %37, 1
  %39 = load i32, ptr %11, align 4
  %40 = srem i32 %38, %39
  %41 = sitofp i32 %40 to double
  %42 = load i32, ptr %11, align 4
  %43 = sitofp i32 %42 to double
  %44 = fdiv double %41, %43
  %45 = load ptr, ptr %17, align 8
  %46 = load i32, ptr %21, align 4
  %47 = sext i32 %46 to i64
  %48 = getelementptr inbounds [1100 x double], ptr %45, i64 %47
  %49 = load i32, ptr %22, align 4
  %50 = sext i32 %49 to i64
  %51 = getelementptr inbounds [1100 x double], ptr %48, i64 0, i64 %50
  store double %44, ptr %51, align 8
  br label %52

52:                                               ; preds = %34
  %53 = load i32, ptr %22, align 4
  %54 = add nsw i32 %53, 1
  store i32 %54, ptr %22, align 4
  br label %30, !llvm.loop !6

55:                                               ; preds = %30
  br label %56

56:                                               ; preds = %55
  %57 = load i32, ptr %21, align 4
  %58 = add nsw i32 %57, 1
  store i32 %58, ptr %21, align 4
  br label %25, !llvm.loop !8

59:                                               ; preds = %25
  store i32 0, ptr %21, align 4
  br label %60

60:                                               ; preds = %91, %59
  %61 = load i32, ptr %21, align 4
  %62 = load i32, ptr %13, align 4
  %63 = icmp slt i32 %61, %62
  br i1 %63, label %64, label %94

64:                                               ; preds = %60
  store i32 0, ptr %22, align 4
  br label %65

65:                                               ; preds = %87, %64
  %66 = load i32, ptr %22, align 4
  %67 = load i32, ptr %12, align 4
  %68 = icmp slt i32 %66, %67
  br i1 %68, label %69, label %90

69:                                               ; preds = %65
  %70 = load i32, ptr %21, align 4
  %71 = load i32, ptr %22, align 4
  %72 = add nsw i32 %71, 1
  %73 = mul nsw i32 %70, %72
  %74 = load i32, ptr %12, align 4
  %75 = srem i32 %73, %74
  %76 = sitofp i32 %75 to double
  %77 = load i32, ptr %12, align 4
  %78 = sitofp i32 %77 to double
  %79 = fdiv double %76, %78
  %80 = load ptr, ptr %18, align 8
  %81 = load i32, ptr %21, align 4
  %82 = sext i32 %81 to i64
  %83 = getelementptr inbounds [900 x double], ptr %80, i64 %82
  %84 = load i32, ptr %22, align 4
  %85 = sext i32 %84 to i64
  %86 = getelementptr inbounds [900 x double], ptr %83, i64 0, i64 %85
  store double %79, ptr %86, align 8
  br label %87

87:                                               ; preds = %69
  %88 = load i32, ptr %22, align 4
  %89 = add nsw i32 %88, 1
  store i32 %89, ptr %22, align 4
  br label %65, !llvm.loop !9

90:                                               ; preds = %65
  br label %91

91:                                               ; preds = %90
  %92 = load i32, ptr %21, align 4
  %93 = add nsw i32 %92, 1
  store i32 %93, ptr %21, align 4
  br label %60, !llvm.loop !10

94:                                               ; preds = %60
  store i32 0, ptr %21, align 4
  br label %95

95:                                               ; preds = %127, %94
  %96 = load i32, ptr %21, align 4
  %97 = load i32, ptr %12, align 4
  %98 = icmp slt i32 %96, %97
  br i1 %98, label %99, label %130

99:                                               ; preds = %95
  store i32 0, ptr %22, align 4
  br label %100

100:                                              ; preds = %123, %99
  %101 = load i32, ptr %22, align 4
  %102 = load i32, ptr %14, align 4
  %103 = icmp slt i32 %101, %102
  br i1 %103, label %104, label %126

104:                                              ; preds = %100
  %105 = load i32, ptr %21, align 4
  %106 = load i32, ptr %22, align 4
  %107 = add nsw i32 %106, 3
  %108 = mul nsw i32 %105, %107
  %109 = add nsw i32 %108, 1
  %110 = load i32, ptr %14, align 4
  %111 = srem i32 %109, %110
  %112 = sitofp i32 %111 to double
  %113 = load i32, ptr %14, align 4
  %114 = sitofp i32 %113 to double
  %115 = fdiv double %112, %114
  %116 = load ptr, ptr %19, align 8
  %117 = load i32, ptr %21, align 4
  %118 = sext i32 %117 to i64
  %119 = getelementptr inbounds [1200 x double], ptr %116, i64 %118
  %120 = load i32, ptr %22, align 4
  %121 = sext i32 %120 to i64
  %122 = getelementptr inbounds [1200 x double], ptr %119, i64 0, i64 %121
  store double %115, ptr %122, align 8
  br label %123

123:                                              ; preds = %104
  %124 = load i32, ptr %22, align 4
  %125 = add nsw i32 %124, 1
  store i32 %125, ptr %22, align 4
  br label %100, !llvm.loop !11

126:                                              ; preds = %100
  br label %127

127:                                              ; preds = %126
  %128 = load i32, ptr %21, align 4
  %129 = add nsw i32 %128, 1
  store i32 %129, ptr %21, align 4
  br label %95, !llvm.loop !12

130:                                              ; preds = %95
  store i32 0, ptr %21, align 4
  br label %131

131:                                              ; preds = %162, %130
  %132 = load i32, ptr %21, align 4
  %133 = load i32, ptr %11, align 4
  %134 = icmp slt i32 %132, %133
  br i1 %134, label %135, label %165

135:                                              ; preds = %131
  store i32 0, ptr %22, align 4
  br label %136

136:                                              ; preds = %158, %135
  %137 = load i32, ptr %22, align 4
  %138 = load i32, ptr %14, align 4
  %139 = icmp slt i32 %137, %138
  br i1 %139, label %140, label %161

140:                                              ; preds = %136
  %141 = load i32, ptr %21, align 4
  %142 = load i32, ptr %22, align 4
  %143 = add nsw i32 %142, 2
  %144 = mul nsw i32 %141, %143
  %145 = load i32, ptr %13, align 4
  %146 = srem i32 %144, %145
  %147 = sitofp i32 %146 to double
  %148 = load i32, ptr %13, align 4
  %149 = sitofp i32 %148 to double
  %150 = fdiv double %147, %149
  %151 = load ptr, ptr %20, align 8
  %152 = load i32, ptr %21, align 4
  %153 = sext i32 %152 to i64
  %154 = getelementptr inbounds [1200 x double], ptr %151, i64 %153
  %155 = load i32, ptr %22, align 4
  %156 = sext i32 %155 to i64
  %157 = getelementptr inbounds [1200 x double], ptr %154, i64 0, i64 %156
  store double %150, ptr %157, align 8
  br label %158

158:                                              ; preds = %140
  %159 = load i32, ptr %22, align 4
  %160 = add nsw i32 %159, 1
  store i32 %160, ptr %22, align 4
  br label %136, !llvm.loop !13

161:                                              ; preds = %136
  br label %162

162:                                              ; preds = %161
  %163 = load i32, ptr %21, align 4
  %164 = add nsw i32 %163, 1
  store i32 %164, ptr %21, align 4
  br label %131, !llvm.loop !14

165:                                              ; preds = %131
  ret void
}

; Function Attrs: noinline nounwind optnone uwtable
define internal void @kernel_2mm(i32 noundef %0, i32 noundef %1, i32 noundef %2, i32 noundef %3, double noundef %4, double noundef %5, ptr noundef %6, ptr noundef %7, ptr noundef %8, ptr noundef %9, ptr noundef %10) #0 {
  %12 = alloca i32, align 4
  %13 = alloca i32, align 4
  %14 = alloca i32, align 4
  %15 = alloca i32, align 4
  %16 = alloca double, align 8
  %17 = alloca double, align 8
  %18 = alloca ptr, align 8
  %19 = alloca ptr, align 8
  %20 = alloca ptr, align 8
  %21 = alloca ptr, align 8
  %22 = alloca ptr, align 8
  %23 = alloca i32, align 4
  %24 = alloca i32, align 4
  %25 = alloca i32, align 4
  store i32 %0, ptr %12, align 4
  store i32 %1, ptr %13, align 4
  store i32 %2, ptr %14, align 4
  store i32 %3, ptr %15, align 4
  store double %4, ptr %16, align 8
  store double %5, ptr %17, align 8
  store ptr %6, ptr %18, align 8
  store ptr %7, ptr %19, align 8
  store ptr %8, ptr %20, align 8
  store ptr %9, ptr %21, align 8
  store ptr %10, ptr %22, align 8
  store i32 0, ptr %23, align 4
  br label %26

26:                                               ; preds = %83, %11
  %27 = load i32, ptr %23, align 4
  %28 = load i32, ptr %12, align 4
  %29 = icmp slt i32 %27, %28
  br i1 %29, label %30, label %86

30:                                               ; preds = %26
  store i32 0, ptr %24, align 4
  br label %31

31:                                               ; preds = %79, %30
  %32 = load i32, ptr %24, align 4
  %33 = load i32, ptr %13, align 4
  %34 = icmp slt i32 %32, %33
  br i1 %34, label %35, label %82

35:                                               ; preds = %31
  %36 = load ptr, ptr %18, align 8
  %37 = load i32, ptr %23, align 4
  %38 = sext i32 %37 to i64
  %39 = getelementptr inbounds [900 x double], ptr %36, i64 %38
  %40 = load i32, ptr %24, align 4
  %41 = sext i32 %40 to i64
  %42 = getelementptr inbounds [900 x double], ptr %39, i64 0, i64 %41
  store double 0.000000e+00, ptr %42, align 8
  store i32 0, ptr %25, align 4
  br label %43

43:                                               ; preds = %75, %35
  %44 = load i32, ptr %25, align 4
  %45 = load i32, ptr %14, align 4
  %46 = icmp slt i32 %44, %45
  br i1 %46, label %47, label %78

47:                                               ; preds = %43
  %48 = load double, ptr %16, align 8
  %49 = load ptr, ptr %19, align 8
  %50 = load i32, ptr %23, align 4
  %51 = sext i32 %50 to i64
  %52 = getelementptr inbounds [1100 x double], ptr %49, i64 %51
  %53 = load i32, ptr %25, align 4
  %54 = sext i32 %53 to i64
  %55 = getelementptr inbounds [1100 x double], ptr %52, i64 0, i64 %54
  %56 = load double, ptr %55, align 8
  %57 = fmul double %48, %56
  %58 = load ptr, ptr %20, align 8
  %59 = load i32, ptr %25, align 4
  %60 = sext i32 %59 to i64
  %61 = getelementptr inbounds [900 x double], ptr %58, i64 %60
  %62 = load i32, ptr %24, align 4
  %63 = sext i32 %62 to i64
  %64 = getelementptr inbounds [900 x double], ptr %61, i64 0, i64 %63
  %65 = load double, ptr %64, align 8
  %66 = load ptr, ptr %18, align 8
  %67 = load i32, ptr %23, align 4
  %68 = sext i32 %67 to i64
  %69 = getelementptr inbounds [900 x double], ptr %66, i64 %68
  %70 = load i32, ptr %24, align 4
  %71 = sext i32 %70 to i64
  %72 = getelementptr inbounds [900 x double], ptr %69, i64 0, i64 %71
  %73 = load double, ptr %72, align 8
  %74 = call double @llvm.fmuladd.f64(double %57, double %65, double %73)
  store double %74, ptr %72, align 8
  br label %75

75:                                               ; preds = %47
  %76 = load i32, ptr %25, align 4
  %77 = add nsw i32 %76, 1
  store i32 %77, ptr %25, align 4
  br label %43, !llvm.loop !15

78:                                               ; preds = %43
  br label %79

79:                                               ; preds = %78
  %80 = load i32, ptr %24, align 4
  %81 = add nsw i32 %80, 1
  store i32 %81, ptr %24, align 4
  br label %31, !llvm.loop !16

82:                                               ; preds = %31
  br label %83

83:                                               ; preds = %82
  %84 = load i32, ptr %23, align 4
  %85 = add nsw i32 %84, 1
  store i32 %85, ptr %23, align 4
  br label %26, !llvm.loop !17

86:                                               ; preds = %26
  store i32 0, ptr %23, align 4
  br label %87

87:                                               ; preds = %145, %86
  %88 = load i32, ptr %23, align 4
  %89 = load i32, ptr %12, align 4
  %90 = icmp slt i32 %88, %89
  br i1 %90, label %91, label %148

91:                                               ; preds = %87
  store i32 0, ptr %24, align 4
  br label %92

92:                                               ; preds = %141, %91
  %93 = load i32, ptr %24, align 4
  %94 = load i32, ptr %15, align 4
  %95 = icmp slt i32 %93, %94
  br i1 %95, label %96, label %144

96:                                               ; preds = %92
  %97 = load double, ptr %17, align 8
  %98 = load ptr, ptr %22, align 8
  %99 = load i32, ptr %23, align 4
  %100 = sext i32 %99 to i64
  %101 = getelementptr inbounds [1200 x double], ptr %98, i64 %100
  %102 = load i32, ptr %24, align 4
  %103 = sext i32 %102 to i64
  %104 = getelementptr inbounds [1200 x double], ptr %101, i64 0, i64 %103
  %105 = load double, ptr %104, align 8
  %106 = fmul double %105, %97
  store double %106, ptr %104, align 8
  store i32 0, ptr %25, align 4
  br label %107

107:                                              ; preds = %137, %96
  %108 = load i32, ptr %25, align 4
  %109 = load i32, ptr %13, align 4
  %110 = icmp slt i32 %108, %109
  br i1 %110, label %111, label %140

111:                                              ; preds = %107
  %112 = load ptr, ptr %18, align 8
  %113 = load i32, ptr %23, align 4
  %114 = sext i32 %113 to i64
  %115 = getelementptr inbounds [900 x double], ptr %112, i64 %114
  %116 = load i32, ptr %25, align 4
  %117 = sext i32 %116 to i64
  %118 = getelementptr inbounds [900 x double], ptr %115, i64 0, i64 %117
  %119 = load double, ptr %118, align 8
  %120 = load ptr, ptr %21, align 8
  %121 = load i32, ptr %25, align 4
  %122 = sext i32 %121 to i64
  %123 = getelementptr inbounds [1200 x double], ptr %120, i64 %122
  %124 = load i32, ptr %24, align 4
  %125 = sext i32 %124 to i64
  %126 = getelementptr inbounds [1200 x double], ptr %123, i64 0, i64 %125
  %127 = load double, ptr %126, align 8
  %128 = load ptr, ptr %22, align 8
  %129 = load i32, ptr %23, align 4
  %130 = sext i32 %129 to i64
  %131 = getelementptr inbounds [1200 x double], ptr %128, i64 %130
  %132 = load i32, ptr %24, align 4
  %133 = sext i32 %132 to i64
  %134 = getelementptr inbounds [1200 x double], ptr %131, i64 0, i64 %133
  %135 = load double, ptr %134, align 8
  %136 = call double @llvm.fmuladd.f64(double %119, double %127, double %135)
  store double %136, ptr %134, align 8
  br label %137

137:                                              ; preds = %111
  %138 = load i32, ptr %25, align 4
  %139 = add nsw i32 %138, 1
  store i32 %139, ptr %25, align 4
  br label %107, !llvm.loop !18

140:                                              ; preds = %107
  br label %141

141:                                              ; preds = %140
  %142 = load i32, ptr %24, align 4
  %143 = add nsw i32 %142, 1
  store i32 %143, ptr %24, align 4
  br label %92, !llvm.loop !19

144:                                              ; preds = %92
  br label %145

145:                                              ; preds = %144
  %146 = load i32, ptr %23, align 4
  %147 = add nsw i32 %146, 1
  store i32 %147, ptr %23, align 4
  br label %87, !llvm.loop !20

148:                                              ; preds = %87
  ret void
}

; Function Attrs: nounwind willreturn memory(read)
declare i32 @strcmp(ptr noundef, ptr noundef) #2

; Function Attrs: noinline nounwind optnone uwtable
define internal void @print_array(i32 noundef %0, i32 noundef %1, ptr noundef %2) #0 {
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca ptr, align 8
  %7 = alloca i32, align 4
  %8 = alloca i32, align 4
  store i32 %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  store ptr %2, ptr %6, align 8
  %9 = load ptr, ptr @stderr, align 8
  %10 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %9, ptr noundef @.str.1)
  %11 = load ptr, ptr @stderr, align 8
  %12 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %11, ptr noundef @.str.2, ptr noundef @.str.3)
  store i32 0, ptr %7, align 4
  br label %13

13:                                               ; preds = %48, %3
  %14 = load i32, ptr %7, align 4
  %15 = load i32, ptr %4, align 4
  %16 = icmp slt i32 %14, %15
  br i1 %16, label %17, label %51

17:                                               ; preds = %13
  store i32 0, ptr %8, align 4
  br label %18

18:                                               ; preds = %44, %17
  %19 = load i32, ptr %8, align 4
  %20 = load i32, ptr %5, align 4
  %21 = icmp slt i32 %19, %20
  br i1 %21, label %22, label %47

22:                                               ; preds = %18
  %23 = load i32, ptr %7, align 4
  %24 = load i32, ptr %4, align 4
  %25 = mul nsw i32 %23, %24
  %26 = load i32, ptr %8, align 4
  %27 = add nsw i32 %25, %26
  %28 = srem i32 %27, 20
  %29 = icmp eq i32 %28, 0
  br i1 %29, label %30, label %33

30:                                               ; preds = %22
  %31 = load ptr, ptr @stderr, align 8
  %32 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %31, ptr noundef @.str.4)
  br label %33

33:                                               ; preds = %30, %22
  %34 = load ptr, ptr @stderr, align 8
  %35 = load ptr, ptr %6, align 8
  %36 = load i32, ptr %7, align 4
  %37 = sext i32 %36 to i64
  %38 = getelementptr inbounds [1200 x double], ptr %35, i64 %37
  %39 = load i32, ptr %8, align 4
  %40 = sext i32 %39 to i64
  %41 = getelementptr inbounds [1200 x double], ptr %38, i64 0, i64 %40
  %42 = load double, ptr %41, align 8
  %43 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %34, ptr noundef @.str.5, double noundef %42)
  br label %44

44:                                               ; preds = %33
  %45 = load i32, ptr %8, align 4
  %46 = add nsw i32 %45, 1
  store i32 %46, ptr %8, align 4
  br label %18, !llvm.loop !21

47:                                               ; preds = %18
  br label %48

48:                                               ; preds = %47
  %49 = load i32, ptr %7, align 4
  %50 = add nsw i32 %49, 1
  store i32 %50, ptr %7, align 4
  br label %13, !llvm.loop !22

51:                                               ; preds = %13
  %52 = load ptr, ptr @stderr, align 8
  %53 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %52, ptr noundef @.str.6, ptr noundef @.str.3)
  %54 = load ptr, ptr @stderr, align 8
  %55 = call i32 (ptr, ptr, ...) @fprintf(ptr noundef %54, ptr noundef @.str.7)
  ret void
}

; Function Attrs: nounwind
declare void @free(ptr noundef) #3

; Function Attrs: nocallback nofree nosync nounwind speculatable willreturn memory(none)
declare double @llvm.fmuladd.f64(double, double, double) #4

declare i32 @fprintf(ptr noundef, ptr noundef, ...) #1

attributes #0 = { noinline nounwind optnone uwtable "frame-pointer"="all" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { nounwind willreturn memory(read) "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #3 = { nounwind "frame-pointer"="all" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+cmov,+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { nocallback nofree nosync nounwind speculatable willreturn memory(none) }
attributes #5 = { nounwind willreturn memory(read) }
attributes #6 = { nounwind }

!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"PIE Level", i32 2}
!3 = !{i32 7, !"uwtable", i32 2}
!4 = !{i32 7, !"frame-pointer", i32 2}
!5 = !{!"Ubuntu clang version 17.0.6 (++20231209124227+6009708b4367-1~exp1~20231209124336.77)"}
!6 = distinct !{!6, !7}
!7 = !{!"llvm.loop.mustprogress"}
!8 = distinct !{!8, !7}
!9 = distinct !{!9, !7}
!10 = distinct !{!10, !7}
!11 = distinct !{!11, !7}
!12 = distinct !{!12, !7}
!13 = distinct !{!13, !7}
!14 = distinct !{!14, !7}
!15 = distinct !{!15, !7}
!16 = distinct !{!16, !7}
!17 = distinct !{!17, !7}
!18 = distinct !{!18, !7}
!19 = distinct !{!19, !7}
!20 = distinct !{!20, !7}
!21 = distinct !{!21, !7}
!22 = distinct !{!22, !7}

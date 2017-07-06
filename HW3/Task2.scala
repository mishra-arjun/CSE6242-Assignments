package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object Task2 {
  def main(args: Array[String]) {
    val sc = new SparkContext(new SparkConf().setAppName("Task2")) //create a SparkContext object, which tells Spark how to access a cluster. 
    //To create a SparkContext you first need to build a SparkConf object that contains information about your application.

    // read the file
    val file = sc.textFile("hdfs://localhost:8020" + args(0)).map(_.split("\t")) //Creating a textfile RDD (Resilient Distributed Data). Args(0) will contain the input file name and location.
    //When this operation is done, the data is not loaded into memory or acted upon in any way. file is just a pointer to the file.
    //Map is a transformation function (functions which create a new RDD). Instead of using x => something, we can use _ to get that line.
    //FLatmap is used to flatten out tuples to values.
    //Map runs each and every element of the dataset through the function and gives a new RDD.

    //Reduce is an action that aggregates all the elements of the RDD using some function.

    val file_filtered = file.filter(lin => lin(2).toInt > 1)
    //This is the final file. 

    //Getting the variables for the addition of target
    val tgt = file_filtered.map(lin => (lin(1), lin(2).toInt))

    val tgt_sum = tgt.reduceByKey(_+_)

    //Getting the variables for the subtraction of the target
    val src = file_filtered.map(lin => (lin(0), 0 - lin(2).toInt))

    val src_sum = src.reduceByKey(_+_)

    //Grouping the two results

    val res = (src_sum++tgt_sum).reduceByKey(_+_)

    //Writing the output file
    val output = res.map{case(a, b) => s"$a\t$b"}

    // store output on given HDFS path.
    output.saveAsTextFile("hdfs://localhost:8020" + args(1))
  }
}
//This is how scala makes writing Map Reduce operations so easy. Instead of writing everything in Java explicitly,
//it does all of the internal working by itself. 